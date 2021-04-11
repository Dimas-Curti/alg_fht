import os


class HTFileReader:
    def __init__(self, file_path, offset):
        self.inputFile = open(file_path, 'rb')
        self.offset = offset
        self.fileSize = os.path.getsize(file_path)

    def read(self, process):
        if self.fileSize < self.offset:
            bs = self.inputFile.read(self.fileSize)
            head_bytes = bs
            tail_bytes = bs
        else:
            self.inputFile.seek(0, 0)
            head_bytes = self.inputFile.read(self.offset)
            self.inputFile.seek(self.fileSize - self.offset, 0)
            tail_bytes = self.inputFile.read(self.offset)

        process(head_bytes, tail_bytes)
        self.stop()

    def stop(self):
        self.inputFile.close()
