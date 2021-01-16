(function() {
    'use strict';

    function TimerServise(){
        EventEmitter2.call(this, { wildcard: true, delimiter: ':' });
        this.start_time = new Date();
        this.end_time = new Date();
    }

    TimerServise.prototype = Object.create(EventEmitter2.prototype);

    TimerServise.prototype.start = function (){
        this.start_time = new Date();
        console.log('Start: '+this.start_time);
    };

    TimerServise.prototype.stop = function (){
        this.end_time = new Date();
        console.log('End: '+this.end_time);
    };

    TimerServise.prototype.start_and_hide = function (){
        this.start();
        document.getElementById('timer-container').style.opacity = 0;
    };

    TimerServise.prototype.stop_and_display = function (){
        this.stop();
        let delta_in_millisecond = this.end_time - this.start_time;
        let old = document.getElementById('time-result').innerText;
        document.getElementById('time-result').innerText = this.time_to_text(delta_in_millisecond)+old;
        document.getElementById('timer-container').style.opacity = 1;
    };

    TimerServise.prototype.time_to_text = function (delta_in_millisecond) {
        var text = '\n';

        text = (delta_in_millisecond % 1000) + ' mill ' + text;
        delta_in_millisecond = parseInt(delta_in_millisecond / 1000);
        text = (delta_in_millisecond % 60) + ' sec, ' + text;
        delta_in_millisecond = parseInt(delta_in_millisecond / 60);
        text = (delta_in_millisecond % 60) +' min, ' + text;
        delta_in_millisecond = parseInt(delta_in_millisecond / 60);
        text = (delta_in_millisecond % 24) + ' hour, ' + text;
        delta_in_millisecond = parseInt(delta_in_millisecond / 24);
        text = delta_in_millisecond + ' days, ' + text;

        return text;
    };

     aidocViewer.services.TimerServise = new TimerServise();
}());