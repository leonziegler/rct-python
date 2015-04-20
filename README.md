# rct-python
Robotics Coordinate Transform (Python)

# Dependencies

1. You will need the `tf2_py` implementation which was split from the roscode. You can find this lib here

> https://github.com/ros/geometry_experimental/tree/indigo-devel/tf2_py

``` bash
export prefix="/tmp/rct"
export prefix_tf2_py="${prefix}/tf2_py"
cd /tmp
git clone https://github.com/ros/geometry_experimental.git
cd geometry_experimental/
mkdir build && cd build
cmake .. -DCMAKE_INSTALL_PREFIX=$prefix_tf2_py
make install -j4
```

2. RSB
See documentation at:

> http://docs.cor-lab.de//rsb-manual/0.11/html/index.html

3. RST
See documentation at:

> http://docs.cor-lab.de//rst-manual/0.11/html/index.html

# Installation

Once you got the environment setup, you can install rct-python easily.

Source your environment and set up your (target) $prefix and install:

``` bash
export prefix="/tmp/rct"
export prefix_rct_python="${prefix}/rct-python/"
python setup.py install --prefix=$prefix
```

# Usage
There are two examples in the examples folder within the repo (will not be installed). See these for a detailed test. They will also work with their C++ counterpart.

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

# Notes
Please note that the future pattern has not yet been implemented in this version. Only past transformations can be obtained.
