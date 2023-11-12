import sys
import requests
import json
import datetime
import dload

def search(query):
  target = "https://api.github.com/search/repositories"
  token = ""
  headers = {
    "Accept": "application/vnd.github+json",
    # "Authorization": f"Bearer {token}",
    "X-GitHub-Api-Version": "2022-11-28"
  }
  params = {
    "q" : query
  }
  r = requests.get(target, params=params, headers=headers)
  result = json.loads(r.text)
  return result

def filterList(data):
  result = []
  star_cnt = 100
  now = datetime.datetime.now()
  days = datetime.timedelta(-30)
  month_before = now + days
  for r in data:
    clone_url = r["clone_url"]
    updated_at = r["updated_at"]
    star = r["stargazers_count"]
    if star < star_cnt:
      continue
    format = "%Y-%m-%dT%H:%M:%SZ"
    date = datetime.datetime.strptime(updated_at, format)
    if date < month_before:
      continue

    print(clone_url)
    result.append(clone_url)

  return result


def writeList(repolist):
  with open("repos.txt", "w") as f:
    for l in repolist:
      f.write(l + "\n")

def cloneList(repolist):
  for l in repolist:
    dload.git_clone(l, "./repos/")

def main():
  if len(sys.argv) != 2:
    print(f"usage: {sys.argv[0]} <query>")

  query = sys.argv[1]
  result = search(query)
  print(f"total: {result['total_count']}")
  repos = filterList(result["items"])
  writeList(repos)
  cloneList(repos)

if __name__ == "__main__":
  main()