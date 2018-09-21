protoc -I=. --python_out=. ./test.proto
python test_proto.py
