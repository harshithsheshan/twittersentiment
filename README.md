# Twittersentiment

The website on clicking "Get started" redirects to the server page.
The page consists of :
1) Query: the keyword or hashtag to search in twitter.
2)starting date : please enter starting date in the format dd mm yyyy 
2)end Date : please enter the end date in the format dd mm yyyy
3) No of tweets to access : it is just a parameter to control the size of database, as we are using a free tier server and sandbox large database is difficult to handle.

The app is hosted on free tier of my amazon web services account, but is accessible from anywhere. Do i still need to host it on the company's aws account ?
If yes please let me know. I will do it by tomorrow.
But as we are using a neo4j sandbox, the service needs to be renewed every 3 days.

The procedure to access neo4j sandbox is as follows. I have added the same on the web-page as well.
 
By opening neo4j browser you can use cypher queries to access graph.On opening the link please click on the link "directly" as it is a shared graph

Enter the following details to access the graph:
host : bolt://ws-10-0-1-175-34336.neo4jsandbox.com:443
Neo4j Graph Username: neo4j

Password: wheel-belt-town

Example Cypher queries:
To view all nodes
match(n)

return(n)

To view all the words in the graph
match(n:word)

return(n)

To view all the tweets in the graph
match(n:word)

return(n)

To view all the categories(sentiment types) in the graph
match(n:word)

return(n)

To view all the words and tweets in the graph
match(n:word),(m:tweet)

return n,m

To view all the nodes with same tweet no
match(n:word),(m:tweet)

where n.tno=m.tno

return n,m

