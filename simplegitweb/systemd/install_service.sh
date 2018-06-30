#!/usr/sh                                                                                                                                                  

if ! [[ `cut -d: -f1 /etc/group | sort |grep 'simplegitweb'` ]]
then
    groupadd simplegitweb
fi

if ! [[ `grep 'simplegitweb' /etc/passwd /etc/shadow` ]]
then
    adduser -r -s /bin/nologin --no-create-home -g simplegitweb simplegitweb
fi

if ! [[ -d '/opt/simplegitweb/' ]]
then
    mkdir -v /opt/simplegitweb/
    chown -Rv simplegitweb:simplegitweb /opt/simplegitweb
fi

if ! [[ -f '/etc/simplegitweb.conf' ]]
then
    cp -fv simplegitweb.conf /etc/simplegitweb.conf
fi


if ! [[ -f '/usr/bin/simplegitweb.py' ]]
then
    cp -fv simplegitweb.py /usr/bin/simplegitweb.py
    chomd +x /usr/bin/simplegitweb.py
fi

cp -fv simplegitweb.service /etc/systemd/system/multi-user.target.wants/simplegitweb.service
systemctl daemon-reload
systemctl enable simplegitweb
systemctl start simplegitweb