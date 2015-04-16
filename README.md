# rct-python
Robotics Coordinate Transform (Python)

# Dependencies

1. You will need the `tf2_py` implementation which was split from the roscode recently. You can find this lib here

> https://github.com/ros/geometry_experimental/tree/indigo-devel/tf2_py

``` bash
cd /tmp
git clone https://github.com/ros/geometry_experimental.git
cd geometry_experimental/
mkdir build && cd build
cmake .. -DCMAKE_INSTALL_PREFIX=/tmp/rct/tf2_py/
make install -j4
```

2. RSB
TODO

3. RST
TODO

4. ProtoBuf
TODO

# Installation

Once you got the environment setup, you can install rct-python easily.

Source your environment so that your (target) $prefix is set. And call:

``` bash
python setup.py install --prefix=$prefix
```
# Usage

``` python
import time
import rct
import logging
logging.basicConfig(level=logging.WARNING)
logging.getLogger('rct').setLevel(logging.INFO)

a = rct.TransformerFactory()

p = a.create_transform_publisher("ExamplePublisher")

t_s = rct.Transform("blub", "parentoruu", "childoruu", time.time())
p.send_transform(t_s, rct.TransformType.STATIC)

t_d = rct.Transform("bla", "leParent", "leChild", time.time())
p.send_transform(t_d, rct.TransformType.DYNAMIC)

r = a.create_transform_receiver()
```
