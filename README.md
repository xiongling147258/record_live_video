1.简介
  使用python和开源库，可以在win7/10/11、rk3399等上录制虎牙视频  
2.如何使用  
 参考如下命令：   
if [ ! -d "/home/xl/files1/record_v2/main.py" ]; then  
     cd /home/xl/files1/record_v2  
     nohup python3 ./main.py  441195 zhajie ./  &  
     nohup python3 ./main.py  52988  bx  ./  &  
     cd /home/xl/files1/record_v2/convert_video  
     nohup python3 main.py /home/xl/files1/record_v2 &  
fi  

