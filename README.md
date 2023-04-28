# AAAS
Aplication As A Service(FYP Project)[updated]

Docker Development Command: docker-compose -f docker-compose-testserver.yml up --build

Docker Production Command: docker-compose up --build

Stripe Listener Command: stripe listen --forward-to localhost:8000/stripe/webhook/


Database Shell Connection: docker-compose exec postgres sh -c 'psql -h postgres -p 5432 -d aaasdatabase -U dbuser' 
RqSTuVWe_TrWEXazxswe_