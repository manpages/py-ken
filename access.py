def getCageId(field, x, y):
  for (id,c) in field['cage']:
    if (x, y) in c['cells']:
      return id
