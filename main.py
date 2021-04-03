from github import Github
import psycopg2
import pathlib
import os


def connect_to_pg():
	try:
		global connection,cursor
		connection = psycopg2.connect(database=os.getenv('POSTGRES_DB'), user=os.getenv('POSTGRES_USER'), password=os.getenv('POSTGRES_PASSWORD')
		, host=os.getenv('PG_HOST'), port=os.getenv('PORT'))
		print("Database opened successfuly")
		cursor=connection.cursor()
		cursor.execute("DROP TABLE IF EXISTS github;")
		connection.commit()
		cursor.execute('''CREATE TABLE github
					(REPOSITORY_NAME CHAR(50) PRIMARY KEY NOT NULL,
					STARS INT NOT NULL,
					PRIMARY_LANGUAGE CHAR(50) NOT NULL);''')
		connection.commit()
		print("github table created successfully")
	except (Exception,psycopg2.Error) as error:
		print("Failed to connect/create table.")
		print("Error:",error)
		cursor.close()
		connection.close()
		print("PostgreSQL connection is closed.")

def insert_to_pg(repo_name,stars,lang):
	try:
		cursor.execute("INSERT INTO github (REPOSITORY_NAME,STARS,PRIMARY_LANGUAGE) VALUES (%s,%s,%s)",(repo_name,stars,lang))
		connection.commit()
		print("Record inserted successfully")
	except (Exception,psycopg2.Error) as error:
		print("Failed to insert data to table.")
		print("Error:",error)
		cursor.close()
		connection.close()
		print("PostgreSQL connection is closed.")
	
	

def close_conn(connection,cursor):
	cursor.close()
	connection.close()
	print("PostgreSQL connection is closed.")
	
def calculate_repos(dict,org):
	for repo in org.get_repos():
		prog_lang=repo.get_languages()
		if prog_lang:
			dict[repo.name+"	"+max(prog_lang , key=prog_lang.get)]=repo.stargazers_count
		else:
			dict[repo.name+"	"+'N/A']=repo.stargazers_count

def main():
	g=Github(os.getenv('ACCESS_TOKEN'))
	org=g.get_organization("kubernetes")
	repo_dict={}
	calculate_repos(repo_dict,org)
	sorted_repos=sorted(repo_dict,key=repo_dict.get,reverse=True)
	print("{:<50} {:<10} {:<20}".format('Repository','Stars','Language'))
	print("------------------------------------------------------------------------")
	for repo in sorted_repos:
		x=repo.split()
		name=x[0]
		language=x[1]
		print("{:<50} {:<10} {:<20}".format(name,repo_dict[repo],language))
	print('\n\n')
	print("adding repositories to postgresql database...")
	connect_to_pg()
	for repo in sorted_repos:
		x=repo.split()
		insert_to_pg(x[0],repo_dict[repo],x[1])
	print("done.")
	close_conn(connection,cursor)

if __name__ == "__main__":
	main()

	
		