import asyncio

async def get_top_skills(skills_data, top_n=3):
    await asyncio.sleep(0)

    skills_list = [(skill, count) for skill, count in skills_data.items()]

    skills_list.sort(key=lambda x: x[1], reverse=True)

    top_skills = {}
    seen_counts = set()

    for skill, count in skills_list:
        if count not in seen_counts:
            top_skills[skill] = count
            seen_counts.add(count)

        if len(top_skills) == top_n:
            break

    final_top_skills = {}
    for skill, count in top_skills.items():
        if list(top_skills.values()).count(count) == 1:
            final_top_skills[skill] = count

    return final_top_skills
