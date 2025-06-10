import { createHash } from 'crypto';
import fs from 'fs';

async function partialMD5(filePath) {
    const step = 1024;
    const size = 1024;
    const hasher = createHash('md5');
    const stats = fs.statSync(filePath);
    const fileSize = stats.size;

    for (let i = -1; i <= 10; i++) {
        const start = Math.min(fileSize, step << (2 * i));
        const end = Math.min(start + size, fileSize);

        if (start >= fileSize) break;

        const fd = fs.openSync(filePath, 'r');
        const buffer = Buffer.alloc(end - start);
        fs.readSync(fd, buffer, 0, buffer.length, start);
        fs.closeSync(fd);
        
        hasher.update(buffer);
    }

    return hasher.digest('hex');
}

// Get file path from command line
const filePath = process.argv[2];
if (!filePath) {
    console.error('Please provide a file path');
    process.exit(1);
}

partialMD5(filePath).then(console.log);
