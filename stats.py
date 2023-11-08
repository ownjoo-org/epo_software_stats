# pylint: disable=missing-docstring, broad-except
from collections import defaultdict
from ast import literal_eval


def main() -> dict:
    results: defaultdict = defaultdict(list)
    errors: list = []
    with open('software-json.txt', 'r') as file:
        while line_raw := file.readline():
            try:
                line = literal_eval(line_raw)
                results[line.get('EPOLeafNode.NodeName')].append(line)
            except Exception as exc_parse:
                errors.append({'error': exc_parse, 'line': line_raw})
    print(f'devices count: {len(results)}')
    print(f'errors count: {len(errors)}')
    return results


if __name__ == '__main__':
    software_totals: defaultdict = defaultdict(int)
    invalid_software_type: int = 0
    invalid_software_name: int = 0
    invalid_software_desc: int = 0
    starts_with_software: int = 0
    skipped: int = 0
    contains_acrobat: list = []
    devices_raw: dict = main()
    devices_count: int = len(devices_raw)

    for device, software in devices_raw.items():
        for each in software:
            software_totals[
                (
                    each.get('MPSDE_SIRSoftwareView.InstallType'),
                    each.get('MPSDE_SIRSoftwareView.GUIDorName'),
                    each.get('MPSDE_SIRSoftwareView.DescriptiveName')
                )
            ] += 1
            if not each.get('MPSDE_SIRSoftwareView.InstallType'):
                invalid_software_type += 1
            if not each.get('MPSDE_SIRSoftwareView.GUIDorName'):
                invalid_software_name += 1
            if not each.get('MPSDE_SIRSoftwareView.DescriptiveName'):
                invalid_software_desc += 1
            sw_type = each.get('MPSDE_SIRSoftwareView.InstallType')
            sw_name = each.get('MPSDE_SIRSoftwareView.GUIDorName')
            if (
                    isinstance(sw_type, str)
                    and sw_type.lower().startswith('software')
            ):
                starts_with_software += 1
            else:
                skipped += 1
            if each and sw_name and 'acrobat' in sw_name.lower():
                contains_acrobat.append({device: each})

    print(f'total unique software: {len(software_totals)}')
    print(f'invalid: all None {software_totals.get((None, None, None))}')
    print(f'invalid: bad type: {invalid_software_type}')
    print(f'invalid: bad name: {invalid_software_name}')
    print(f'invalid: bad desc: {invalid_software_desc}')
    print(f'contain "acrobat": {len(contains_acrobat)}')
    print(f'starts with "software": {starts_with_software}')
    print(f'skipped: {skipped}')
