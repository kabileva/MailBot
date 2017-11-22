from database.database import get_email

i = 1
data = get_email(i)
while data is not None:
	print(str(i)+': '+data[3])
	i += 1
	data = get_email(i)
