FROM ubuntu
MAINTAINER dante-signal31 (dante.signal31@gmail.com)
# Abort on error.
RUN set -e
# Install coko.
RUN apt-get update && \
    apt-get install apt-transport-https && \
    echo "deb [trusted=yes] https://dl.bintray.com/dante-signal31/deb generic main" | sudo tee -a /etc/apt/sources.list && \
    apt-key adv --keyserver pgp.mit.edu --recv-keys 379CE192D401AB61 && \
    apt-get update && \
    apt-get install coko
# Prepare test bed.
RUN adduser alan && \
    adduser bob && \
    mkdir /home/alan/coko_test/ && \
    mkdir /home/alan/coko_test/folder1 && \
    mkdir /home/alan/coko_test/folder2 && \
    mkdir /home/alan/coko_test/folder1/folder3/ && \
    echo "1111" >> /home/alan/coko_test/executable && \
    echo "2222" >> /home/alan/coko_test/config && \
    echo "3333" >> /home/alan/coko_test/folder1/data1 && \
    echo "4444" >> /home/alan/coko_test/folder1/data2 && \
    echo "5555" >> /home/alan/coko_test/folder2/data3 && \
    echo "6666" >> /home/alan/coko_test/folder1/folder2/data4 && \
    chown alan /home/alan/coko_test -R && \
    mkdir /home/bob/coko_test/ && \
    mkdir /home/bob/coko_test/folder1 && \
    mkdir /home/bob/coko_test/folder2 && \
    mkdir /home/bob/coko_test/folder1/folder3/ && \
    echo "aaaa" >> /home/bob/coko_test/executable && \
    echo "bbbb" >> /home/bob/coko_test/config && \
    echo "cccc" >> /home/bob/coko_test/folder1/data1 && \
    echo "dddd" >> /home/bob/coko_test/folder1/data2 && \
    echo "eeee" >> /home/bob/coko_test/folder2/data3 && \
    echo "ffff" >> /home/bob/coko_test/folder1/folder2/data4 && \
    chown bob /home/bob/coko_test -R && \