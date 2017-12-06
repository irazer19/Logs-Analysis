import psycopg2
from datetime import datetime


def connect():
    """Connects to the PostgreSQL database and returns the connection."""
    return psycopg2.connect("dbname=news")


def popular_article():
    """ Method to execute the sql query for the question:
    What are the most popular three articles of all time? """
    db = connect()
    c = db.cursor()
    c.execute("select pop_article.title, count(pop_article.path) as\
               total from (select articles.title, log.path from articles,\
               log where replace(log.path, '/article/', '')=articles.slug)\
               as pop_article group by pop_article.title order by total desc\
               limit 3;")
    article = c.fetchall()
    db.close()
    return article


def popular_author():
    """ Method to execute the sql query for the question:
    Who are the most popular article authors of all time?"""
    db = connect()
    c = db.cursor()
    c.execute("select authors.name, count(pop_author.path) from authors,\
               (select articles.author, log.path from articles, log where\
               replace(log.path, '/article/', '')=articles.slug) as\
               pop_author where authors.id=pop_author.author group by\
               authors.name order by count desc limit 4;")
    author = c.fetchall()
    db.close()
    return author


def error():
    """ Method to execute the sql query for the question:
    On which days did more than 1% of requests lead to errors?"""
    db = connect()
    c = db.cursor()
    c.execute("select result.date, result.error*100.0/total as percent from\
               (select total_error.date, total_error.count as error,\
               total_status.count as total from (select substring\
               (cast(log.time as varchar),1,10) as date,count(log.status)\
               from log group by date) as total_status inner join\
              (select substring(cast(log.time as varchar),1,10) as date,\
              count(log.status) from log where log.status!='200 OK' group\
              by date) as total_error on total_status.date=total_error.date)\
              as result order by percent desc limit 1;")
    error = c.fetchall()
    db.close()
    return error

""" Runs the programme if it is called from the main python file """
if __name__ == '__main__':
    articles = popular_article()
    # Converting the output of the most famous articles into string format
    articles = [[str(item) for item in article] for article in articles]
    # Printing the output of the most famous article
    print('\nQ1. What are the most popular three articles of all time?\
           \n\n' + ' views\n'.join([' -- '.join(article) for article in
          articles]) + ' views\n')

    authors = popular_author()
    # Converting the output of the most famous authors into string format
    authors = [[str(item) for item in author] for author in authors]
    # Printing the output of the most famous authors
    print('Q2. Who are the most popular article authors of all time?\
           \n\n' + ' views\n'.join([' -- '.join(author) for author in
          authors]) + ' views\n')

    error = error()
    # Extracting the date from error list and changing its format
    date = error[0][0]
    date = datetime.strptime(date, '%Y-%m-%d')
    # Printing the output of the errors more than 1%
    print('Q3. On which days did more than 1% of requests lead to errors?\
          \n\n' + date.strftime("%B %d, %Y") + " -- " + str(error[0][1])
          [:4] + " % errors")
