#source ~/venvs/willenv/bin/activate && jupyter notebook
# do `act` to run alias from bash profile that sources will
# do `deact` to disable

#jupyter notebook
#jupyter notebook > notebook.log 2>&1 &
#/usr/bin/xvfb-run --auto-servernum --server-num=1 -s "-screen 0 1400x900x24" jupyter notebook > notebook.log 2>&1 &

#source /home/ubuntu/anaconda3/bin//activate pytorch_p36 && /usr/bin/xvfb-run --auto-servernum --server-num=1 -s "-screen 0 1400x900x24" jupyter notebook > notebook.log 2>&1 &

xvfb-run --auto-servernum --server-num=1 -s "-screen 0 1400x900x24" jupyter notebook > notebook.log 2>&1 &
