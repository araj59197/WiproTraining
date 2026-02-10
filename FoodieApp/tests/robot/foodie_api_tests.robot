***Settings***
Library        RequestsLibrary
Suite Setup    Create Session     foodie    http://localhost:5000

***Variables***
${BASE_URL}    http://localhost:5000

***Test Cases***
Register Restaurant
    [Documentation]               Test registering a new restaurant
    ${data}=                      Create Dictionary                    name=Robot Restaurant    category=Indian        location=Mumbai    contact=9999999999
    ${response}=                  POST On Session                      foodie                   /api/v1/restaurants    json=${data}
    Status Should Be              201                                  ${response}
    Should Be Equal As Strings    ${response.json()}[name]             Robot Restaurant

View Restaurant
    [Documentation]               Test viewing restaurant profile
    ${data}=                      Create Dictionary                  name=View Restaurant             category=Chinese                        location=Delhi    contact=8888888888
    ${create_response}=           POST On Session                    foodie                           /api/v1/restaurants                     json=${data}
    ${restaurant_id}=             Set Variable                       ${create_response.json()}[id]
    ${response}=                  GET On Session                     foodie                           /api/v1/restaurants/${restaurant_id}
    Status Should Be              200                                ${response}
    Should Be Equal As Strings    ${response.json()}[name]           View Restaurant

Add Dish
    [Documentation]               Test adding a dish to a restaurant
    ${restaurant_data}=           Create Dictionary                     name=Dish Restaurant                 category=Italian                               location=Pune              contact=7777777777
    ${restaurant_response}=       POST On Session                       foodie                               /api/v1/restaurants                            json=${restaurant_data}
    ${restaurant_id}=             Set Variable                          ${restaurant_response.json()}[id]
    ${dish_data}=                 Create Dictionary                     name=Pasta                           type=Main Course                               price=250
    ${response}=                  POST On Session                       foodie                               /api/v1/restaurants/${restaurant_id}/dishes    json=${dish_data}
    Status Should Be              201                                   ${response}
    Should Be Equal As Strings    ${response.json()}[name]              Pasta

Register User
    [Documentation]               Test user registration
    ${data}=                      Create Dictionary            name=Robot User      email=robot@example.com    password=robotpass
    ${response}=                  POST On Session              foodie               /api/v1/users/register     json=${data}
    Status Should Be              201                          ${response}
    Should Be Equal As Strings    ${response.json()}[email]    robot@example.com

Place Order
    [Documentation]            Test placing an order
    ${user_data}=              Create Dictionary        name=Order User                      email=order@example.com           password=pass
    ${user_response}=          POST On Session          foodie                               /api/v1/users/register            json=${user_data}
    ${user_id}=                Set Variable             ${user_response.json()}[id]
    ${restaurant_data}=        Create Dictionary        name=Order Restaurant                category=Fast Food                location=Bangalore         contact=6666666666
    ${restaurant_response}=    POST On Session          foodie                               /api/v1/restaurants               json=${restaurant_data}
    ${restaurant_id}=          Set Variable             ${restaurant_response.json()}[id]
    ${dish_item}=              Create Dictionary        dish_id=${1}                         quantity=${2}
    @{dishes_list}=            Create List              ${dish_item}
    ${order_data}=             Create Dictionary        user_id=${user_id}                   restaurant_id=${restaurant_id}    dishes=${dishes_list}
    ${response}=               POST On Session          foodie                               /api/v1/orders                    json=${order_data}
    Status Should Be           201                      ${response}

Approve Restaurant
    [Documentation]               Test admin approving a restaurant
    ${restaurant_data}=           Create Dictionary                    name=Approve Restaurant              category=Cafe                                         location=Chennai           contact=5555555555
    ${restaurant_response}=       POST On Session                      foodie                               /api/v1/restaurants                                   json=${restaurant_data}
    ${restaurant_id}=             Set Variable                         ${restaurant_response.json()}[id]
    ${response}=                  PUT On Session                       foodie                               /api/v1/admin/restaurants/${restaurant_id}/approve
    Status Should Be              200                                  ${response}
    Should Be Equal As Strings    ${response.json()}[message]          Restaurant approved

View All Orders Admin
    [Documentation]     Test admin viewing all orders
    ${response}=        GET On Session                   foodie         /api/v1/admin/orders
    Status Should Be    200                              ${response}

Health Check
    [Documentation]               Test health check endpoint
    ${response}=                  GET On Session                foodie         /health
    Status Should Be              200                           ${response}
    Should Be Equal As Strings    ${response.json()}[status]    healthy
