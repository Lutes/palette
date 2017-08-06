app.controller('HomeController', ['$scope', function($scope){
	$scope.uploadFile = function(){
        var file = $scope.myFile;
        console.log('file is ' );
        console.dir(file);
        var uploadUrl = "/fileUpload";
        fileUpload.uploadFileToUrl(file, uploadUrl);
    };

    // this.uploadFileToUrl = function(file, uploadUrl){
    //     var fd = new FormData();
    //     fd.append('file', file);
    //     $http.post(uploadUrl, fd, {
    //         transformRequest: angular.identity,
    //         headers: {'Content-Type': undefined}
    //     })
    //     .success(function(){
    //     })
    //     .error(function(){
    //     });
    // };

}]);