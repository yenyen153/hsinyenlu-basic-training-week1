def log_in(Session,Crawlerlog):
    with Session() as session:
        with open(Crawlerlog, "r", encoding='utf-8') as log_file:
            logs = log_file.readlines()
            try:
                for log in logs:
                    match = re.match(r"([\d-]+ [\d:,]+) (.+)", log)

                    if match:
                        time = match.group(1)
                        message = match.group(2)
                        time_log = {'time':time, 'message':message}
                        session.add(CrawlerLog(**time_log))
            except Exception as e:
                pass

        session.commit()