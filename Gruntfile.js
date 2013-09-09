module.exports = function(grunt) {

    grunt.initConfig({
        pkg: grunt.file.readJSON('package.json'),
        less: {
            options: {
                paths: ['<%= pkg.resources %>bootstrap-3.0.0/less/', '<%= pkg.name %>/resources/less/*']
            },
            default: {
                files: {
                    "<%= pkg.name %>/resources/css/styles.css": "<%= pkg.name %>/resources/less/styles.less",
                }
            }
        },
        watch: {
            files: ['<%= pkg.name %>/resources/less/*'],
            tasks: ['less'],
        },
    });

    /*
    grunt.event.on('watch', function(action, filepath, target) {
        grunt.log.writeln(target + ': ' + filepath + ' has ' + action);
    });
    */

    grunt.loadNpmTasks('grunt-contrib-watch');
    grunt.loadNpmTasks('grunt-contrib-less');
    grunt.loadNpmTasks('grunt-notify');
    //grunt.loadNpmTasks('grunt-contrib-imagemin');

    grunt.registerTask('default', ['less']);

};
