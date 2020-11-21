from validate_email import validate_email
is_valid = validate_email(email_address='jaroslav.matyas@jaga.sk', \
    check_regex=True, check_mx=True, \
    from_address='my@from.addr.ess', helo_host='doma.sk', \
    smtp_timeout=10, dns_timeout=10, use_blacklist=True)

print(is_valid)
