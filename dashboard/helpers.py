
def find_parent_keys(d, target_key, parent_key=None):
    for k, v in d.items():
        if k == target_key:
            yield parent_key
        if isinstance(v, dict):
            for res in find_parent_keys(v, target_key, k):
                yield res


class EconomicEnums:
    costs_total = 0
    annuity_total = 1
    costs_upfront_in_year_zero = 2
    annuity_om = 3
    levelized_cost_of_energy_of_asset = 4


