def addReview(m_name, v_email, comment, rating, cursor):
	query = "INSERT INTO museumDB.review VALUES ('{0}', '{1}', '{2}', {3});".format(m_name, v_email, comment, rating)
	#TODO Add error handling
	print(query)
	cursor.execute(query)
