import csv
import json
import io

i = 1
result = []
with open('restaurants_tiny.csv', 'rb') as f:
    reader = csv.reader(f)
    for row in reader:
        result.append({
            'model': 'editorial.restaurant',
            'pk': i,
            'fields': {
                'mongo_id': row[0],
                'title': row[1],
            }
        }) 
        i += 1
        
with io.open('restaurants_tiny.json', 'w', encoding='utf-8') as f:
    data = json.dumps(result, ensure_ascii=False).decode('utf-8')
    f.write(unicode(data)) 
    
              
