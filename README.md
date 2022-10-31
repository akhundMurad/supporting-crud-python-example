
# Example of supporting application on Python

Inspired by [Eric Evans](https://www.amazon.com/Domain-Driven-Design-Tackling-Complexity-Software/dp/0321125215) and [Vladik Khononov's](https://www.amazon.com/Learning-Domain-Driven-Design-Aligning-Architecture/dp/1098100131) books.

The purpose of this repository is to show the way of implementing supporting enterprise applications
 in the [Python programming language](https://github.com/python).


**_Feel free to contribute!_**

# About sctructure of application
### What is supporting application?
A domain is consists of multiple subdomains. Each subdomain corresponds to a different part of the business.
According to Domain Driven Design there are 3 types of subdomains:
1. Core subdomains - are one of the most important subdomains for business. That is what differentiates your product from products of competitors.
2. Generic subdomains - are also important for business, but there are a lot of ready-for-use solutions. There is no need for optimization and every competitor does it in the same way. For example, authentication/authorization systems or message brokers.
3. Supporting subdomains - are the subdomains which have no ready-for-use solutions and also have no complex logic. This type of subdomain doesn't give any competitive advantage to the business side. 

Usually, to implement core applications, developers use complex patterns (such as Aggregate, CQRS, Event Sourcing and so on), but for supporting applications there is no need to do so. We can use much simpler patterns, such as [Transaction Script](https://martinfowler.com/eaaCatalog/transactionScript.html) for domain layer.

# Run Locally

1. Clone the project

```bash
  git clone https://github.com/akhundMurad/supporting-crud-python-example.git
```

2. Create virtual environment

```bash
  python -m venv .venv
  source .venv/bin/activate
```

3. Set environment variables ([example](envfiles/.envfile.example))

4. Install dependencies

```bash
  pip install -r requirements.txt
```

5. Apply migrations

```bash
  alembic upgrade head
```

6. Start the server

```bash
  uvicorn src.presentation.api.asgi:asgi
```

# Links
https://www.amazon.com/Domain-Driven-Design-Tackling-Complexity-Software/dp/0321125215

https://www.amazon.com/Learning-Domain-Driven-Design-Aligning-Architecture/dp/1098100131

https://medium.com/nick-tune-tech-strategy-blog/domains-subdomain-problem-solution-space-in-ddd-clearly-defined-e0b49c7b586c
