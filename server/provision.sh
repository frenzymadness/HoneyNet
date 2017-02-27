#!/bin/bash

# be root
sudo su

# disable SELinux
echo -e "SELINUX=disabled\nSELINUXTYPE=targeted" > /etc/selinux/config

# change root password
echo "pass1234" | passwd --stdin root

# install packages
dnf --assumeyes install vsftpd

# enable anonymous upload
sed -i 's/#anon_upload_enable=YES/anon_upload_enable=YES/g' /etc/vsftpd/vsftpd.conf
# Fix permissions on uploaded files
echo -e "chown_uploads=YES\nchown_upload_mode=0644\nchown_username=ftp" >> /etc/vsftpd/vsftpd.conf
# chmod on public directory
chmod 777 /var/ftp/pub

# start FTP
service vsftpd start

# run after reboot
chkconfig vsftpd on

# reboot
reboot
