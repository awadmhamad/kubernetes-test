from github import Github
import pathlib

def calc_lang(prog_lang,file):
	file_extension=pathlib.Path(file.name).suffix
	count=prog_lang.get(file_extension)
	if count==None:
		prog_lang[file_extension]=file.size
	else:
		count+=file.size
		prog_lang.update({file_extension: count})

def calculate(repo,dict):
	print('start Calculating...')
	prog_lang={}
	contents=repo.get_contents("")
	count=0
	while contents:
		count+=1
		file_content = contents.pop(0)
		print(count)
		print(file_content)
		if file_content.type == "dir":
			contents.extend(repo.get_contents(file_content.path))
		else:
			calc_lang(prog_lang,file_content)
	dict[repo.name+" "+max(prog_lang.iteritems(), key=operator.itemgetter(1))[0]]=repo.stargazers_count
	print(repo.name+"	"+max(prog_lang.iteritems(), key=operator.itemgetter(1))[0]+"	"+repo.stargazers_count)
	print('ended calculating')

def sort_repos(dict,org):
	for repo in org.get_repos():
		calculate(repo,dict)

def main():
	g=Github(os.getenv(ACCESS_TOKEN))
	org=g.get_organization("kubernetes")
	repo_dict={}
	sort_repos(repo_dict,org)
	for repo in repo_dict:
		print(repo+"	"+repo_dict[repo])

if __name__ == "__main__":
	main()

	
		