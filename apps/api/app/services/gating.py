def add_gates(model, found, gates, pick, start, end):
    """A picked action needs a picked road finished first; open routes are ungated."""
    for item in found:
        route = gates[item["id"]]
        if route is None:
            continue
        via = []
        for road in route:
            ready = model.NewBoolVar(f"via_{road}_{item['id']}")
            if road in pick:
                model.AddImplication(ready, pick[road])
                model.Add(end[road] <= start[item["id"]]).OnlyEnforceIf(ready)
            else:
                model.Add(ready == 0)
            via.append(ready)
        model.AddBoolOr(via).OnlyEnforceIf(pick[item["id"]])
