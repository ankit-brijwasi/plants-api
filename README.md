# Plants app backend API's

> LIVE APPLICATION DEMO AT: [https://plants-app--api.herokuapp.com](https://plants-app--api.herokuapp.com)

**FOR PROTECTED ROUTES HEADER SHOULD CONTAIN THE AUTHORIZATION TOKEN IN THE GIVEN FORMAT**

`Authorization: Token *your token here*`

Endpoints-

1.  /api/auth/registration/

    ALLOWED METHODS: POST

    Request body should contain-

        - email
        - password1
        - first_name
        - last_name
        - user_type ("user"/"nursury")

    Response-

        {
            "key": "",
            "user": {
                "first_name": "",
                "last_name": "",
                "email": "",
                "type": ""
            },
            "created": ""
        }

2.  /api/auth/login/

    ALLOWED METHODS: POST

    Request body should contain-

        - email
        - password

    Response-

        {
            "key": "",
            "user": {
                "first_name": "",
                "last_name": "",
                "email": "",
                "type": ""
            },
            "created": ""
        }

3.  /api/nursury/ - **[Protected Route]**

    > THIS ROUTE IS ONLY ALLOWED FOR NURSURIES

    ALLOWED METHODS: GET, POST, PATCH, DELETE

    **GET: _returns the plants added by this nursury_**

    > To get a single plant request to- `/api/nursury/:plant_id`

        Response-
            [
                {
                    id: plant_id,
                    name: "",
                    image: "",
                    price: "",
                    user: user_id,
                },
                {
                    id: plant_id,
                    name: "",
                    image: "",
                    price: "",
                    user: user_id,
                },
                ...
            ]

    **POST: _adds a new plant_**

        Request body should contain-
            - name
            - image
            - price

        Response-
            {
                id: plant_id,
                name: "",
                image: "",
                price: "",
                user: user_id,
            }

    **PATCH: _updates plant_**

    > add the plant_id in the url

    > syntax: `/api/nursury/:plant_id/`

        Request body should contain-
            fields that needs to be changed

        Response-
             {
                id: plant_id,
                name: "",
                image: "",
                price: "",
                user: user_id,
            }

    **DELETE: _Deletes plant_**

    > add the plant_id in the url

    > syntax: `/api/nursury/:plant_id/`

        Response-
            204 NO CONTENT [if the plant is found, otherwise 404]

4.  /api/nursury/plants/ - **[Protected Route]**

    ALLOWED METHODS: GET

    > To get a single plant request to- `/api/nursury/plants/:plant_id`

        Response-
            [
                {
                    id: plant_id,
                    name: "",
                    image: "",
                    price: "",
                    user: user_id,
                },
                {
                    id: plant_id,
                    name: "",
                    image: "",
                    price: "",
                    user: user_id,
                },
                ...
            ]

5.  /api/cart/ - **[Protected Route]**

    ALLOWED METHODS: GET, PUT, DELETE

    **GET: _returns user's cart_**

        Response-
            {
                "id": cart_id,
                "placed_by": { ...logged_in_user },
                "details": [
                    {
                        "id": cart_details_id,
                        "quantity": quantity,
                        "price": price,
                        "plant": { ...plant }
                    },
                    {
                        "id": cart_details_id,
                        "quantity": quantity,
                        "price": price,
                        "plant": { ...plant }
                    },
                    ...
                ],
                "status": "CART",
                "ordered_on": null
            }

    **PUT: _creates and updates user's cart_**

        Request data-
            details: [
                {
                    plant: plant_id,
                    quantity: 1,
                },
                {
                    plant: plant_id,
                    quantity: 1,
                },
                ...
            ]


        Response-
            {
                "id": cart_id,
                "placed_by": { ...logged_in_user },
                "details": [
                    {
                        "id": cart_details_id,
                        "quantity": quantity,
                        "price": price,
                        "plant": { ...plant }
                    },
                    {
                        "id": cart_details_id,
                        "quantity": quantity,
                        "price": price,
                        "plant": { ...plant }
                    },
                    ...
                ],
                "status": "CART",
                "ordered_on": null
            }

    **DELETE: _deletes user's cart and also removes item from the cart_**

        Response-
            204 NO CONTENT [if the cart is found, otherwise 404]

        To delete an item of the cart, send the following information via query_params-
            - delete=item
            - id=:plant_id to be removed

        example-

            DELETE /api/cart/?delete=item&id=1

6.  /api/orders/generate/ - **[Protected Route]**

        ALLOWED METHODS: GET

        Response-
            {
                "id": cart_id,
                "placed_by": { ...logged_in_user },
                "details": [
                    {
                        "id": cart_details_id,
                        "quantity": quantity,
                        "price": price,
                        "plant": { ...plant }
                    },
                    {
                        "id": cart_details_id,
                        "quantity": quantity,
                        "price": price,
                        "plant": { ...plant }
                    },
                    ...
                ],
                "status": "ORDERED",
                "ordered_on": date
            }

7.  /api/orders/complete/ - **[Protected Route]**

    > THIS ROUTE IS ONLY ACCESSIBLE FOR THE ADMIN

    ALLOWED METHODS: POST

        Request body must contain-
            - cart_id

        Response-
            {
                "id": cart_id,
                "placed_by": { ...logged_in_user },
                "details": [
                    {
                        "id": cart_details_id,
                        "quantity": quantity,
                        "price": price,
                        "plant": { ...plant }
                    },
                    {
                        "id": cart_details_id,
                        "quantity": quantity,
                        "price": price,
                        "plant": { ...plant }
                    },
                    ...
                ],
                "status": "DELIVERED",
                "ordered_on": date
            }

8.  /api/order/view/ - **[Protected Route]**

    > THIS ROUTE IS ONLY ACCESSIBLE FOR NURSURIES

    ALLOWED METHODS: GET

        Response-

        {
            "active_orders": [
                {
                    ...order_details,
                    status: "ORDERED"
                },
                {
                    ...order_details,
                    status: "ORDERED"
                },
                ...
            ],
            "orders_deliverd": [
                {
                    ...order_details,
                    status: "DELIVERED"
                },
                {
                    ...order_details,
                    status: "DELIVERED"
                },
                ...

            ]
        }
