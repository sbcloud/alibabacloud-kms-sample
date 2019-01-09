// Test OSS server side encryption feature.
package main

import (
	"fmt"
	"os"
	"strings"

	"github.com/aliyun/aliyun-oss-go-sdk/oss"
)

const (
	// TokyoOSSEndPoint is the Tokyo region endpoint
	TokyoOSSEndPoint = "https://oss-ap-northeast-1.aliyuncs.com"
	// AccessKeyID should should not be included in a source code like this
	AccessKeyID = "<Your AccessKeyId>"
	// AccessKeySecret should not be included in a source code like this
	AccessKeySecret = "<Your AccessKeySecret>"
)

func handleError(err error) {
	fmt.Println("Error:", err)
	os.Exit(-1)
}
func main() {
	bucketName := "<Your Bucket>"

	// Initialize the client
	client, err := oss.New(TokyoOSSEndPoint, AccessKeyID, AccessKeySecret)
	if err != nil {
		handleError(err)
	}

	// Get the bucket
	bucket, err := client.Bucket(bucketName)
	if err != nil {
		handleError(err)
	}

	// Upload a file to OSS with server side encryption enabled. We use OSS and KMS integration feature to automatically encrypt file on upload.
	// For every region, if server side encryption is used for the first time with KMS, OSS will automatically create am encryption key on KMS first. KMS must be activated before this operation.
	err = bucket.PutObject("test.txt", strings.NewReader("Never Give Up - Jack Ma."), oss.ServerSideEncryption("KMS"))
	if err != nil {
		handleError(err)
	}

	// We can then get the object and print it to verify that it has been encrypted using a key generated on KMS
	object, err := bucket.GetObject("test.txt")
	if err != nil {
		handleError(err)
	}
	fmt.Print(object)
}