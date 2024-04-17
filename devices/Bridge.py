def install_Bridge():



#  ont add 14 20 sn-auth "48575443ED03ED9D" omci ont-lineprofile-id 4 ont-srvprofile-id 111 desc "CELENIA QUINTERO 0000008395" 
#  ont optical-alarm-profile 14 20 profile-id 3
#  ont alarm-policy 14 20 policy-id 1
#  ont ipconfig 14 20 ip-index 2 dhcp vlan 2241 priority 5
#  ont internet-config 14 20 ip-index 2
#  ont wan-config 14 20 ip-index 2 profile-id 0
#  ont policy-route-config 14 20 profile-id 2
#  ont fec 14 20 use-profile-config 
#  ont port native-vlan 14 20 eth 1 vlan 2241 priority 0 
# #
# [bbs-config]
#   <bbs-config>
#  service-port 35430 vlan 2241 gpon 0/3/14 ont 20 gemport 11 multi-service user-vlan 2241 tag-transform transparent inbound traffic-table index 111 outbound traffic-table index 111