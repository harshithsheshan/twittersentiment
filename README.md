# Twittersentiment
By opening neo4j browser you can use cypher queries to access graph.On opening the link please click on the link "directly" as it is a shared graph

Enter the following details to access the graph:
host :https://10-0-1-175-34337.neo4jsandbox.com/

Neo4j Graph USername: neo4j

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

