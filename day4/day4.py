"""
Day 4
"""

class Passport:
    def __init__(self, batch_file_str: str):
        """
        byr (Birth Year)
        iyr (Issue Year)
        eyr (Expiration Year)
        hgt (Height)
        hcl (Hair Color)
        ecl (Eye Color)
        pid (Passport ID)
        cid (Country ID)
        """
        self.byr = None
        self.iyr = None
        self.eyr = None
        self.hgt = None
        self.hcl = None
        self.ecl = None
        self.pid = None
        self.cid = None
        
        already_set_keys = set()
        splitted  = batch_file_str.split()
        if len(splitted) > 8:
            raise ValueError("Okay, there can be duplicates!")
        for s in splitted:
            key_val_split = s.split(':')
            key, val = key_val_split[0], key_val_split[1]
            if key in already_set_keys:
                raise ValueError("Fuck, duplicates!")
            already_set_keys.add(key)
            if key == 'byr':
                self.byr = val
            elif key == 'iyr':
                self.iyr = val
            elif key == 'eyr':
                self.eyr = val
            elif key == 'hgt':
                self.hgt = val
            elif key == 'hcl':
                self.hcl = val
            elif key == 'ecl':
                self.ecl = val
            elif key == 'pid':
                self.pid = val
            elif key == 'cid':
                self.cid = val
            else:
                raise ValueError("Unknown passport property: " + key)

    def check_byr(self):
        return len(self.byr) == 4 and int(self.byr) >= 1920 and int(self.byr) <= 2002

    def check_iyr(self):
        return len(self.iyr) == 4 and int(self.iyr) >= 2010 and int(self.iyr) <= 2020

    def check_eyr(self):
        return len(self.eyr) == 4 and int(self.eyr) >= 2020 and int(self.eyr) <= 2030

    def check_hgt(self):
        if self.hgt is None:
            return False
        unit = self.hgt[-2:]
        num = int(self.hgt[:-2])
        return (unit == 'cm' and num >= 150 and num <= 193 or unit == 'in' and num >= 59 and num <= 76)

    def check_hcl(self):
        prefix = self.hcl[0]
        if prefix != '#':
            return False
        rest = self.hcl[1:]
        if len(rest) != 6:
            return False
        for c in rest:
            if not (c >= '0' and c <= '9' or c >= 'a' and c  <= 'f'):
                return False
        return True

    def check_ecl(self):
        possible = ["amb", "blu", "brn", "gry", "grn", "hzl", "oth"]
        return self.ecl in possible

    def check_pid(self):
        return len(self.pid) == 9

    def has_required_fields(self):
        return self.byr is not None and self.check_byr() and self.iyr is not None and self.check_iyr() and self.eyr is not None and self.hgt is not None and \
                self.hcl is not None and self.ecl is not None and self.pid is not None and self.check_eyr() and self.check_hgt() and self.check_hcl() and \
                self.check_ecl() and self.check_pid()

    def __str__(self):
        return f'byr={self.byr},iyr={self.iyr},eyr={self.eyr},hgt={self.hgt},hcl={self.hcl},ecl={self.ecl},pid={self.pid},cid={self.cid}'


def read_input(path: str) -> list:
    out = []
    with open(path, 'r') as file:
        next_batch_file = file.readline()[:-1]
        while True:
            line = file.readline()
            if line == '' and next_batch_file == '':
                break
            
            if line == '\n' or line == '':
                print("About to add some stuff!") # FIXME:
                out.append(Passport(next_batch_file))
                print(out[-1])  # FIXME:
                next_batch_file = ''
            else:
                next_batch_file += ' ' +  line[:-1]
    return out


def solve(input: list) -> int:
    valid_passports = 0
    for passport in input:
        if passport.has_required_fields():
            valid_passports += 1
    return valid_passports        


if __name__ == '__main__':
    input = read_input('/Users/danielgrittner/development/advent-of-code2020/day4/input.txt')
    print(solve(input))

