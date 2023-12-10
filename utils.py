import random

def main():
    get_distribution(3)

# 20 Lines
# Sections with descriptions:
# Experience
#   - 1-3 sections
# Projects
#   - 1-3 sections
# Total of 5 sections
def get_distribution(year):
    # Returns a dictionary detailing how many lines each section should get,
    # In order to keep the length to one page
    class_factor = None
    match year:
        case 1:
            class_factor = 0.4
        case 2:
            class_factor = 0.7
        case 3:
            class_factor = 1
        case 4:
            class_factor = 1.5

    num_experiences = round(random.random() * 3 * class_factor)
    num_experiences = min(num_experiences, 3)
    num_projects = 5 - num_experiences
    # print(f"This person has {num_experiences} experiences")
    # print(f"This person has {num_projects} projects")

    min_lines = 2
    max_lines = 5
    total_lines = 20
    sections = set([0, 1, 2, 3, 4])
    d = {s: min_lines for s in sections}

    for i in range(total_lines - min_lines * len(sections)):
        section = random.choice(list(sections))
        d[section] += 1
        if d[section] >= max_lines:
            sections.remove(section)

    # print(d)
    # print(f"Sum of d is {sum(d.values())}")

    r = {
        "experiences": [],
        "projects": [],
    }
    for k, v in d.items():
        if k < num_experiences:
            r['experiences'].append(v)
        else:
            r['projects'].append(v)

    # print(r)
    return r


if __name__ == "__main__":
    main()