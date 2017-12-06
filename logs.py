#!/usr/bin/env python
from datetime import datetime
import psycopg2


def connect():
    """Connects to the PostgreSQL database and returns the connection."""
    return psycopg2.connect("dbname=news")


def popular_article():
    """ Method to execute the sql query for the question:
    What are the most popular three articles of all time? """
    db = connect()
    c = db.cursor()
    c.execute("""SELECT pop_article.title, COUNT(pop_article.path) AS
               total FROM (SELECT articles.title, log.path FROM articles,
               log WHERE replace(log.path, '/article/', '')=articles.slug)
               AS pop_article GROUP BY pop_article.title ORDER BY total DESC
               LIMIT 3;""")
    article = c.fetchall()
    db.close()
    return article


def popular_author():
    """ Method to execute the sql query for the question:
    Who are the most popular article authors of all time?"""
    db = connect()
    c = db.cursor()
    c.execute("""SELECT authors.name, COUNT(pop_author.path) FROM authors,
               (SELECT articles.author, log.path FROM articles, log WHERE
               replace(log.path, '/article/', '')=articles.slug) AS
               pop_author WHERE authors.id=pop_author.author GROUP BY
               authors.name ORDER BY count DESC LIMIT 4;""")
    author = c.fetchall()
    db.close()
    return author


def error():
    """ Method to execute the sql query for the question:
    On which days did more than 1% of requests lead to errors?"""
    db = connect()
    c = db.cursor()
    c.execute("""SELECT result.date, result.error*100.0/total AS percent FROM
               (SELECT total_error.date, total_error.count AS error,
               total_status.count AS total FROM (SELECT substring
               (cast(log.time AS VARCHAR),1,10) as date,COUNT(log.status)
               FROM log GROUP BY date) AS total_status INNER JOIN
               (SELECT substring(cast(log.time AS VARCHAR), 1, 10) AS date,
               COUNT(log.status) FROM log WHERE log.status!='200 OK' group
               by date) AS total_error ON total_status.date=total_error.date)
               AS result ORDER BY percent DESC LIMIT 1;""")
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
