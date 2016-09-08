# -*- coding: utf-8 -*-

from glob import glob
from srl import SRL

def test_rules():
    for filename in glob('tests/rules/*.rule'):
        with open(filename) as f:
            fdata = f.read()
            in_capture = False
            data = {'srl': None, 'matches': [], 'no_matches': [], 'captures': {}}
            for line in fdata.splitlines():
                if not line or line.startswith('#'):
                    continue
                if in_capture and not line.startswith('-'):
                    in_capture = False
                if line.startswith('srl: '):
                    data['srl'] = line[5:]
                elif line.startswith('match: "'):
                    data['matches'].append(line[8:-1])
                elif line.startswith('no match: "'):
                    data['no_matches'].append(line[11:-1])
                elif line.startswith('capture for "') and line.endswith('":'):
                    in_capture = line[13:-2]
                elif in_capture and line.startswith('-'):
                    split = line[1:].split(': ')
                    index = int(split[0].strip())
                    name = split[1].strip()
                    matching = split[2][1:-1]
                    data['captures'].setdefault(in_capture, {})
                    if name == '0':
                        data['captures'][in_capture].setdefault(index, [])
                        data['captures'][in_capture][index].append(matching)
                    else:
                        data['captures'][in_capture].setdefault(index, {})
                        data['captures'][in_capture][index][name] = matching
            srl = SRL(data['srl'])
            for match in data['matches']:
                assert srl.search(match), match
            for no_match in data['no_matches']:
                assert not srl.search(no_match), no_match
            for capture, matches in data['captures'].items():
                for index, expected in matches.items():
                    if isinstance(expected, list):
                        assert expected[0] == srl.findall(capture)[index]
                    else:
                        groupindex = srl.groupindex
                        all = srl.findall(capture)
                        for key, val in expected.items():
                            find_val = srl.findall(capture)[index]
                            if isinstance(find_val, str):
                                assert val == find_val
                            else:
                                assert val == find_val[groupindex[key] - 1]
