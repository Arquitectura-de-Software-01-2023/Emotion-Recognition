const AWS = require('aws-sdk');
const parseMultipart = require('parse-multipart');
const { v4: uuidv4 } = require('uuid');

const BUCKET = process.env.BUCKET;

const s3 = new AWS.S3();

module.exports.imageUploadHandler = async (event) => {
    try {
        console.log('Beginning of the function');
        const { filename, data } = extractFile(event);
        console.log('Filename: ' + filename);
        const { newFilename, response } = fileNameValidation(filename);
        if (response !== undefined) {
            return response;
        }
        console.log('New filename: ' + newFilename);
        const params = {
            Bucket: BUCKET,
            Key: newFilename,
            ACL: 'public-read',
            Body: data,
        };
        console.log('Uploading file to S3');
        await s3.putObject(params).promise();
        console.log('File uploaded to S3');

        return {
            statusCode: 200,
            body: JSON.stringify({
                data: {
                    filename: newFilename,
                    url: `https://${BUCKET}.s3.amazonaws.com/${newFilename}`,
                },
                message: 'File uploaded successfully',
                successful: true,
            }),
        };
    } catch (err) {
        return {
            statusCode: 500,
            body: JSON.stringify({
                data: null,
                message: err.message,
                successful: false,
            }),
        };
    }
};

function extractFile(event) {
    const boundary = parseMultipart.getBoundary(event.headers['Content-Type']);
    const files = parseMultipart.Parse(Buffer.from(event.body, 'base64'), boundary);
    const [{ filename, data }] = files;
    return { filename, data };
}

function fileNameValidation(filename) {
    let response;
    const typeMatch = filename.match(/\.([^.]*)$/);
    console.log('Type match: ' + typeMatch);
    if (!typeMatch) {
        response = {
            statusCode: 403,
            body: JSON.stringify({
                data: null,
                message: 'File must have an extension',
                successful: false,
            }),
        };
    }
    const fileType = typeMatch[1];
    console.log('File type: ' + fileType);
    if (fileType !== 'jpg' && fileType !== 'png' && fileType !== 'jpeg') {
        response = {
            statusCode: 403,
            body: JSON.stringify({
                data: null,
                message: 'File must be an image',
                successful: false,
            }),
        };
    }
    const newFilename = `${uuidv4()}.${fileType}`;
    return { newFilename, response };
}
