# annuaire

scrap and collect address from lawyers

### Requirements

Install docker, docker-compose and docker-machine

### Installation

Copy env.template to .env and fill variables

Create a symbolic link with the docker-compose file you want to use. 

   ```
   ln -s docker-compose-dev.yml docker-compose.yml
   ```
   
Launch the server:
  
  ```
      docker-compose build
      docker-compose up -d
  ```
  
  - The api use the uri /api.
  - The webapp use the uri /.
  - Swagger is available at the uri /api/doc.html
   
   
### Manual commands:


Launch unitary tests:

**Only in dev environnement**

   ```
      docker-compose exec python manage test
   ```

Check pep violations:

**Only in dev environnement**

   ```
      docker-compose exec python manage lint
   ```

   