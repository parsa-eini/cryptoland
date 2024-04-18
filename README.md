# RUN
run docker-compose up

# TEST #
- You can use the postman collection export which is in the main directory

# NOTE
## There are 2 different implementations for international exchange settlements. Each have PROS & CONS
## we can choose one of the options by changing the value of USE_PERIODIC_TASK which is in settings file
* POST SAVE SIGNAL of ORDER
    * It is good since we do the settlement as soon
    as possible but may cause database overhead since we should check the threshold after each purchase
* PERIODIC TASK
    * It is good in case we have more users and orders since it will check the threshold
    with intervals but the main disadvantage is that the settlement will not happen ASAP

