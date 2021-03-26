# sequence
Manage sequences of frame numbers

## Install

```bash
pip install cioseq
```

## Usage

Import
```
>>> from cioseq.sequence import Sequence
```

Several ways to create a Sequence using the `create()` factory method.
```
# [start [end [step]]] - Unlike range(), end is inclusive.

>>> s = Sequence.create("1")

>>> s = Sequence.create(1,10,2)

# list
>>> s = Sequence.create([5,6,7,10,12])

# spec
>>> s = Sequence.create("1-10x2")

# compound spec with negative frame numbers
>>> s = Sequence.create("0-10x3, 100, -10--2x2")

# Copy constructor
>>> s2 = Sequence.create(s)
>>> s2 == s
False
>>> list(s2) == list(s)
True

>>> list(s)
[-10, -8, -6, -4, -2, 0, 3, 6, 9, 100]

>>> print(s)
-10-0x2,3-9x3,100

>>> repr(s)
"Sequence.create('-10-0x2,3-9x3,100')"
```

Indexing
```
>>> s[-1]
100

s[0]
-10
```

An arithmetic progression is a set of numbers with a common step.
```
>>> s = Sequence.create([1,4,7,10,13])
>>> type(s)
<class 'cioseq.sequence.Progression'>

>>> s=Sequence.create([1,2,3,5,78])
>>> type(s)
<class 'cioseq.sequence.Sequence'>
>>> s.is_progression()
False

```

Chunks
```
# Split into chunks, which are themselves Sequences.
>>> s = Sequence.create("1-20", chunk_size=5)
>>> s.chunk_count()
4
>>> s.chunks()
[Sequence.create('1-5'), Sequence.create('6-10'), Sequence.create('11-15'), Sequence.create('16-20')]

# Chunks can be cyclic.
>>> s.chunk_strategy = "cycle"
>>> for c in s.chunks():
...    print(list(c))

[1, 5, 9, 13, 17]
[2, 6, 10, 14, 18]
[3, 7, 11, 15, 19]
[4, 8, 12, 16, 20]
```

Booleans
```
>>> s = Sequence.create("1-10")
>>> isect = s.intersection(range(5, 15))
>>> print(isect)
5-10


>>> s = Sequence.create("1-10")
>>> uni = s.union(range(5, 15))
>>> print(uni)
1-14

```

Intersecting chunks. Helps to determine which tasks contain scout frames.

```
>>> s = Sequence.create("1-50", chunk_size=5)
>>> scout =  Sequence.create("1,2,7")
>>> chunks = s.intersecting_chunks(scout)
>>> print(chunks)
[Sequence.create('1-5'), Sequence.create('6-10')]
```

Multi sequence filename permutations

```
# single sequence
>>> template = "/path/%(frame)d/image.%(frame)04d.tif"
>>> filenames = list(Sequence.permutations(template, frame="0-6x2"))
>>> print(filenames)
['/path/0/image.0000.tif', '/path/2/image.0002.tif', '/path/4/image.0004.tif', '/path/6/image.0006.tif']

# several sequences
>>> template = "image_%(uval)02d_%(vval)02d.%(frame)04d.tif"
>>> kw = {"uval": "1-2", "vval": "1-2", "frame": "10-11"}
>>> filenames = Sequence.permutations(template, **kw)

>>> print(filenames)
<generator object permutations at 0x10260f960>

>>> for f in filenames:
...    print f

image_01_01.0010.tif
image_01_02.0010.tif
image_02_01.0010.tif
image_02_02.0010.tif
image_01_01.0011.tif
image_01_02.0011.tif
image_02_01.0011.tif
image_02_02.0011.tif
```

Offset
```
>>> s = Sequence.create("1-10")
>>> s = s.offset(-5)
>>> print(s)
-4-5
```

Hash (#) filename expansion

```
>>> s = Sequence.create("8-10")
s.expand("image.#.exr")
['image.8.exr', 'image.9.exr', 'image.10.exr']

s.expand("/some/dir_###/img.#####.exr")
['/some/dir_008/img.00008.exr', '/some/dir_009/img.00009.exr', '/some/dir_010/img.00010.exr']
```

Dollar(n)F filename expansion

```
>>> s = Sequence.create("1")
>>> s.expand_dollar_f("image.$F.exr")
['image.1.exr']

>>> s.expand_dollar_f("image.$F.$5F.$2F.exr")
['image.1.00001.01.exr']

```

Use different symbols for frame spec
```
>>> s = Sequence.create("1-10, 14, 20-48x4")
>>> print(s)
1-10,14,20-48x4

>>> print(s.to(":", "%", ";"))
1:10;14;20:48%4

>>> print(s.to("to", "by", " "))
1to10 14 20to48by4

```

Take a subsample of frames
```
s = Sequence.create("1-10")
>>> print(s.subsample(1))
6

>>> print(s.subsample(2))
3-8x5

>>> print(s.subsample(3))
2-6x4,9

>>> print(s.subsample(5))
2-10x2

>>> print(list(s.subsample(4)))
[2, 4, 7, 9]
```

## Test

From git repo
```
python -m unittest discover -v -s ./tests  -p 'test_*.py'
```

## Contributing


Clone the repo.

```
git clone git@github.com:ConductorTechnologies/cioseq.git
cd cioseq
```

Set up a clean virtual envirionment with Python 2.7 for development (optional).

```
python -m virtualenv venv
. ./venv/bin/activate
```

Install development dependencies
```
pip install -r requirements_dev.txt
```

pip install --upgrade . 

```

## License
[MIT](LICENSE)
