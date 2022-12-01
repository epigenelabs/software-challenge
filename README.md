## 🐍 Track Backend

In that track, we will explore the API and try to improve it.

### Level 0

Make sure you can query the API. We use Postman at Epigene Labs, but feel free to use the tool you want.

Create a couple of Genesets to get more familiar with it. 

---
> Answer

In Postman, set the URL as `http://127.0.0.1:8000/genesets`, and the method as `POST`, and put the dict below in the body as JSON format.
```
{
    "title": "test_geneset_title",
    "genes": [
        {
            "name": "test_gene_name1"
        },
        {
            "name": "test_gene_name2"
        }
    ]
}
```

### Level 1

Now as a user, let's say you want to retrieve a gene based on its name, and know in which genesets it is present. 

Update the API so that we can deliver that new feature.

---
> Answer

In `crud.py`, write functions `get_genes` and `get_gene_by_name` to perform SQL queries from db to retrieve corredsponding data. 
Then, in `main.py`, write functions `read_all_genes` and `read_match_genes` as `GET` method to render the data from `crud.py`. Note the data structure of response data is `list`.

### Level 2

Sometimes, users don't know the specific name of a gene. They might not be able to retrieve correctly the gene they are looking for thanks to the previous API's update in Level 1. 

Update the API with a way to allow a user to search for genes.

---
> Answer

We can either apply approximate matching in SQL query, using `LIKE`, or suggest the users to search a specific gene by its `id`.
To search by `id`, do the same as previous step, write SQL query in `crud.py` and render in with a function in `main.py`. Note the data structure of repsonse data now is `dict`, a single gene item.

### Level 3

We like to be able to search Geneset by title.Let's say you have a Geneset with title `Great Genes`, you could search and retrieve it with: 

````
127.0.0.1:8000/genesets/search/Great
````
Make sure it works as expected.

Now, we have thousands of users. 

Run `poetry run python populate.py` to populate the database and simulate the number of users. 

Let's check again the endpoint that allow a user to retrieves the full list of genesets. The output doesn't look good, and it's getting slower right ? 

Suggest a way to improve it.

---
> Answer

If I'm not mistaken, the output doesn't become much slower. I checked `populate.py`, the script seemed only to scale the data in db, not to scale the users or client calls.

To simulate the concurrent calls, I've added client side multiproccessing, multithreading and async scripts to call the api. Theoretically, they should be a lot faster than regular synchronous calls, but I don't know why they are not as fast as I expected. But you can get my ideas, and do it on the server side, so they can respond to massive calls concurrently.

Besides, pagination and caching are alternatives to reduce single response time. This should be the simplest way.

Ultimately, we can create server clusters, which should be more complicated and unfortunately I have no experience at the moment.

### Level 4 - Bonus

Let's be real, this API isn't best in class. How do you think we could improve it ?

The idea here is not to implement any solution. Just think of some improvements we could discuss during the interview.

---
> Answer

1. The search endpoints can be better. Already marked in the code.
2. If they're open to external partners, we need authentication as a middleware, or even different authorizations for different users.
3. I imagine gene data can be complicated and contain many attributes, so, we can break down users' needs and only respond with necessary data for each request.
4. Use connection pooling. It's like caching. Caching lowers the latency by avoiding repeated calls to endpoints; connection pooling do it by avoiding frequent visits to db.
5. Add a logging in case we further need to analyze the requests.
