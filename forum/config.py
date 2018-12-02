config = {
    'SESSION_TYPE': 'memcached',
    'SQLALCHEMY_DATABASE_URI':
        'mysql+mysqlconnector://wustl_inst:'
        'wustl_pass@ec2-52-14-93-16.us-east-2.compute.amazonaws.com:3306/orm_forum',
    'SQLALCHEMY_TRACK_MODIFICATIONS': True,
    'SESSION_COOKIE_HTTPONLY': True,
    'SECRET_KEY': 'super secret key',
    'MAX_AGE': 3600,
}
