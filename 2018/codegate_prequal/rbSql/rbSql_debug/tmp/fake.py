data = "\x02\x02\x01\x0brbSqlSchema\x01\x0c/rbSqlSchema" 
# type length data

f = open("rbSqlSchema", "wb")
f.write(data)
f.close()
