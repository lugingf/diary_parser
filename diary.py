import requests
import webbrowser
from bs4 import BeautifulSoup


def diary():
	session = requests.Session()
	headers = {'Referer': 'https://www.mos.ru/pgu/ru/application/dogm/journal/'}
	auth_url = "https://mrko.mos.ru/dnevnik/services/index.php"
	connected = False
	maxattempt = 10
	attempt = 1
	while not connected and attempt < maxattempt:
		try:
			print('Trying to connect')
			auth_req = session.get(auth_url, headers=headers, params={"login":login, "password":MD5_PASSWORD}, allow_redirects=False)
			connected = True
		except requests.exceptions.ConnectionError:
			attempt +=1
			print(' ConnectionError...\nTrying one more time')
		else:
			print('Connected')
	main_req = session.get("https://mrko.mos.ru/dnevnik/services/dnevnik.php?r=1&first=1")
	parsed_html = BeautifulSoup(main_req.content, 'lxml')
	columns = parsed_html.body.find_all('div', 'b-diary-week__column')
	final_ans = []
	for column in columns:
		date_word = column.find("div", "b-diary-week-head__title").find_all("span")[0].text
		# суббота всегда пустая, поэтому ее можно пропустить
		if date_word == 'СУББОТА':
			pass
		else:
			date_number = column.find("span", "b-diary-date").text
			title = '<h3>' + date_number + ' ' +  date_word + '</h3>'
			final_ans.append(title)
			lessons_table = column.find("div", "b-diary-lessons_table")
			all_lists = lessons_table.find_all("div", "b-dl-table__list")
			for lesson in all_lists:
				lesson_columns = lesson.find_all("div", "b-dl-td_column")
				lesson_number = lesson_columns[0].span.text
				lesson_name = lesson_columns[1].span.text
				# Если название урока пусто, пропускаем
				if lesson_name == "":
					pass
				else:
					lesson_dz = lesson_columns[2].find("div", "b-dl-td-hw-section").span.text
					lesson_mark = lesson_columns[3].span.text[0:1]
					lesson_comment = lesson_columns[4].find("div", "b-dl-td-hw-comments").span.text
					final_ans.append(
											"<b>{0}. {1}</b>. Домашнее задание:\n"
											"<i>{2}</i>\n"
											"Оценка за урок: <b>{3}</b> <sub>{4}</sub>\n\n".format(lesson_number,
																					lesson_name,
																					lesson_dz,
																					lesson_mark,
																					lesson_comment))
			final_ans.append("\n-------------------\n\n")
	return final_ans
		
if __name__ == '__main__':
	result_fl_name = 'DIAR.html'
	week_data = diary()
	with open(result_fl_name, 'w', encoding='utf-8') as f:
		for d in week_data:
			txt = '<div>' + d + '</div>'
			f.write(txt)
		print('Data stored at {}'.format(result_fl_name))
	print('Opening result data in your default browser...')
	webbrowser.open(result_fl_name)
		