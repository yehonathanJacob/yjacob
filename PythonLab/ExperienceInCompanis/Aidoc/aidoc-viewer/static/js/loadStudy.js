function loadStudy(seriesViewer, viewportModel, studyUid, containerEl) {

    $(seriesViewer).find('.undock-toolbox-button').hide();
    $(seriesViewer).find('.undock-toolbox-button').on('click', function(event) {
        event.preventDefault();
        aidocViewer.services.ToolboxService.open();
        return false;
    });

    $(seriesViewer).find('.call-support-link').on('click', function(e) {
        aidocViewer.utils.supportUtils.showSupportDialog();
        return false;
    });

    if (aidocViewer.services.ConfigService.showSupportLink) {
        $(seriesViewer).find('.call-support-link-container').removeClass('hidden');
    }

    // Initialze change tracking (autosave, undo/redo)
    aidocViewer.services.ChangeLogService.reset(true);

    if( aidocViewer.services.ConfigService.isDemo){
        $(seriesViewer).find('.scan-state-modify-toolbar').hide();
        $(seriesViewer).find('.add-finding-btn-group').hide();
        $(seriesViewer).find('.user-findings-panel').hide();
        $(seriesViewer).find('.scan-action-bar').hide();
    }
    openToolbox();
    addKeyBindings();

    var progressBar = new LoadingOverlayProgress({
        bar: {
            bottom: 0,
            height: '20px',
            background: '#fe5b14'
        },
        text: {
            display: 'none'
        }
    });
    $(containerEl).LoadingOverlay('show', {
        image       : '',
        color       : 'black',
        fade        : [0, 600],
        fontawesome : 'fa fa-spinner fa-pulse',
        custom      : progressBar.Init()
    });

    function progressNotifier(percentage) {
        progressBar.Update(percentage);
    }


    aidocViewer.services.ScanService.loadStudy(studyUid, progressNotifier)
        .catch(function(e) {
            delete progressBar;
            $(containerEl).LoadingOverlay('hide', true);
            throw e;
        })
        .then(function(data) {
            delete progressBar;
            $(containerEl).LoadingOverlay('hide', true);
            var study = data.study;
            var scans = data.scans;
            var findings = data.findings;

            // Init viewports
            var viewportManager = aidocViewer.services.ViewportManager;
            viewportManager.init(seriesViewer, viewportModel, onLayoutChange);


            var seriesId = 0;
            var firstScan = null;
            for (var seriesUid in scans) {
                if (scans.hasOwnProperty(seriesUid)) {
                    var scan = scans[seriesUid];
                    if (firstScan == null){
                        firstScan = scan;
                    }

                    viewportManager.stacks.push(prepareScanStack(scan.uid, scan, seriesId));
                    seriesId++;
                }
            }

            // Add a stack containing only our findings to the stacks array
            viewportManager.stacks.push(prepareFindingsStack(findings, seriesId));

            // Enable auto save
            aidocViewer.services.ChangeLogService.setAutoSave(true);

             if (seriesId > 1) {
                viewportManager.setLayout('study');
            } else {
                viewportManager.setLayout('series');
            }
            setupSeriesViewerTitle(study, firstScan.uid, viewportManager);

            // setup the tool buttons
            setupButtons(seriesViewer);

            // Sends the timing hit to Google Analytics.
            var scanLoadTime = Math.round(aidocViewer.utils.timingUtils.stop());
            ga('send', 'timing', 'Scan', 'load', scanLoadTime);

            sendLoadMetricsToServer(studyUid,scanLoadTime);

            if (aidocViewer.services.WindowManager.isSecondaryWindowOpen()) {
                // TODO: This needs to happen every time the secondary window is opened (after setLayout)
                aidocViewer.services.WindowManager.secondaryWindowPromise.then(function(secondaryWindow) {
                    var doc = $(secondaryWindow.document);
                    setupButtons(doc.find('.series-viewer'));
                    doc.find('.scan-patient-name').text(study.patientName);
                    doc.find('.patient-location-name').text(study.patientLocation);
                    doc.find('.series-uid').text(main_series_uid);
                    doc.find('.accession-number').text(study.accessionNumber);
                });
            }

            // check if report should be loaded automatically
            if (aidocViewer.services.ConfigService.autoLoadReport){
                showStudyReport()
            }

            // layout choose
            $(seriesViewer).find('.choose-layout a').click(function() {
                disableAllTools();

                var previousUsed = [];

                viewportManager.forEachViewport(function(el, vp, i) {
                    if (!isNaN($(el).data('useStack'))) {
                        previousUsed.push($(el).data('useStack'));

                        aidocViewer.tools.findingsScrollSynchronizer.remove(el);
                    }
                });

                var type = $(this).text();
                viewportManager.setLayout(type);

//                if (previousUsed.length > 0) {
//                    previousUsed = previousUsed.slice(0, viewportManager.viewports.length);
//                    var item = 0;
//
//                    previousUsed.forEach(function(v) {
//                        useItemStack(item++, v);
//                    });
//                }

                return false;
            });

            function sendLoadMetricsToServer(studyUid, loadTime) {
                $.ajax({
                    url: '/api/loaded-study',
                    type: 'POST',
                    contentType: 'application/json; charset=utf-8',
                    dataType: 'json',
                    data: JSON.stringify({
                        study_uid: studyUid,
                        load_time: loadTime
                    })
                });
            }

            function setupSeriesViewerTitle(study, main_series_uid, viewportManager) {
                // Set the scan details in the header
                $(seriesViewer).find('.scan-patient-name').text(study.patientName);
                $(seriesViewer).find('.patient-location-name').text(study.patientLocation);

                $(seriesViewer).find('.series-uid').text(main_series_uid);
                $(seriesViewer).find('.accession-number').text(study.accessionNumber);


                // register for main vieport change
                viewportManager.forEachViewport(function (el, vp, i) {
                    $(vp).on('MainViewportChanged', function () {
                        if (viewportManager.getMainScanViewportIdx() === i) {
                            $(seriesViewer).find('.series-uid').text(viewportManager.stacks[i].seriesUid);
                        }
                    });
                });
            }
            function useItemStack(item, stack) {
                var element = viewportManager.getElement(item);

                if ($(element).data('waiting')) {
                    viewportManager.viewports[item].find('.overlay-text').remove();
                    $(element).data('waiting', false);
                }

                $(element).data('useStack', stack);

                if (viewportManager.getFindingsViewportIdx() === item) {
                    viewportManager.updateFindingViewport(item);
                    $(element).data('setup', true);
                    return;
                }

                var imageId = viewportManager.stacks[stack].imageIds[0];

                if (!$(element).data('setup')) {
                    return cornerstone.loadImage(imageId).then(function(image) {
                        setupViewport(element, viewportManager.stacks[stack], image);
                        setupViewportOverlays(element, null, true);

                        aidocViewer.tools.findingsScrollSynchronizer.add(element);

                        if (viewportManager.getMainScanViewportIdx() === item) {
                            aidocViewer.tools.keySliceIndicator.enable(element);
                        }

                        $(element).on('MainViewportChanged', function() {
                            if (viewportManager.getMainScanViewportIdx() === item) {
                                aidocViewer.tools.keySliceIndicator.enable(element);
                            } else {
                                aidocViewer.tools.keySliceIndicator.disable(element);
                            }
                        });

                        // Enable findings tool
                        aidocViewer.tools.finding.enable(element);
                        aidocViewer.tools.finding.deactivate(element, 1);

                        // Show reference lines if displaying multiple planes
                        if (aidocViewer.services.ViewportManager.layout.type === 'study') {
                            aidocViewer.utils.referenceLines.init(element);
                        }

                        $(element).data('setup', true);
                        $(element).trigger('CornerstoneNewScan');
                    });
                }
            }
            // Resize series viewer
            function resizeSeriesViewer(seriesViewer) {
                // Resize the parent div of the viewport to fit the screen
                var imageViewerElement = $(seriesViewer).find('.imageViewer')[0];
                var parentDiv = $(seriesViewer).find('.viewer')[0];
                $(imageViewerElement).css({height : $(parentDiv).height() - $(parentDiv).find('.text-center:eq(0)').height()});

                viewportManager.forEachViewport(function(el, vp) {
                    cornerstone.resize(el, false);

                    if(cornerstone.getEnabledElement(el).image) {
                        aidocViewer.utils.fitToWindowEx(el);
                    }

                    if ($(el).data('waiting')) {
                        var ol = vp.find('.overlay-text');
                        if (ol.length < 1) {
                            ol = $('<div class="overlay overlay-text">Loading series...</div>').appendTo(vp);
                        }
                    }
                }, true, seriesViewer);
            }

            function onLayoutChange(isFirstChange) {
                openToolbox();
                initViewports();
                resizeSeriesViewer(seriesViewer);

                aidocViewer.services.ViewportManager.forEachViewport(function(element, viewport, index) {
                    useItemStack(index, index);
                });

                if (aidocViewer.services.WindowManager.isSecondaryWindowOpen()) {
                    aidocViewer.services.WindowManager.secondaryWindowPromise.then(function(secondaryWindow) {
                        resizeSeriesViewer($(secondaryWindow.document).find('#seriesViewerTemplate'));

                        if (isFirstChange) {
                            var largestFinding = showLargestFindingSlice(findings);
                            showRepresentativeSliceInScanViewports(largestFinding);

                        }
                    });
                } else {
                    if (isFirstChange) {
                        var largestFinding = showLargestFindingSlice(findings);
                        showRepresentativeSliceInScanViewports(largestFinding);

                    }
                }
            }

            // Call resize viewer on window resize
            $(window).resize(function() {
                resizeSeriesViewer(seriesViewer);
            });
        });

    function showLargestFindingSlice(findings) {
        for (var seriesId in findings) {
            if (findings.hasOwnProperty(seriesId)) {
                var findingsMetadata = findings[seriesId];

                if(findingsMetadata.length == 0){
                    continue
                }
                var largestFinding = findingsMetadata[0];

                var keySlice = largestFinding.key_slice;
                var seriesMetadata = aidocViewer.services.ScanService.getSeriesMetadata(largestFinding.series_id);

                var uid = seriesMetadata.uid;

                aidocViewer.services.ViewportManager.forEachFindingViewport(function (element) {
                    var stackData = cornerstoneTools.getToolState(element, 'stack');
                    if (!stackData || !stackData.data || !stackData.data.length) {
                        return null;
                    }

                    var imageIds = stackData.data[0].imageIds;

                    for (var i = 0; i < imageIds.length; i++) {
                        var imageInfo = aidocViewer.utils.imageIdUtils.split(imageIds[i]);
                        if (imageInfo.uid === uid && imageInfo.sliceNum === keySlice) {
                            cornerstoneTools.scrollToIndex(element, i);
                        }
                    }
                }, true);

                return largestFinding;
            }
        }

        return null;

    }


    function showRepresentativeSliceInScanViewports(largestFinding) {
        aidocViewer.services.ViewportManager.forEachScanViewport(function(element) {
            var stackToolDataSource = cornerstoneTools.getToolState(element, 'stack');
            if (!stackToolDataSource || !stackToolDataSource.data || !stackToolDataSource.data.length) {
                return null;
            }

            var stackData = stackToolDataSource.data[0];
            if (!stackData.imageIds.length) {
                return;
            }

            if(largestFinding){
                aidocViewer.utils.finding.gotoFinding(largestFinding);
            }
            else {
                cornerstoneTools.scrollToIndex(element, Math.floor(stackData.imageIds.length / 2));
            }

        });
    }

    function initViewports() {
        var viewportManager = aidocViewer.services.ViewportManager;
        viewportManager.forEachViewport(function(el) {
            cornerstone.enable(el);
        });

        // Enable the toolbox for the findings stack
        var viewportEl = viewportManager.getElement(viewportManager.getMainScanViewportIdx());
        aidocViewer.services.ToolboxService.enable(viewportEl);
    }

    function openToolbox() {
        if (aidocViewer.services.WindowManager.isSecondaryWindowOpen()) {
            aidocViewer.services.WindowManager.secondaryWindowPromise.then(function(secondaryWindow) {
                aidocViewer.services.ToolboxService.openInline(secondaryWindow);
            });
        } else {
            aidocViewer.services.ToolboxService.openInline();
        }
    }


    function showStudyReport() {
        var study = aidocViewer.services.ScanService.study;
        var studyReport = study.report;

        if (!studyReport || studyReport.length == 0) {
            toastr.options = {
                "closeButton": false,
                "debug": false,
                "newestOnTop": false,
                "progressBar": false,
                "positionClass": "toast-top-center",
                "preventDuplicates": true,
                "onclick": null,
                "showDuration": "300",
                "hideDuration": "1000",
                "timeOut": "1500",
                "extendedTimeOut": "0",
                "showEasing": "swing",
                "hideEasing": "linear",
                "showMethod": "fadeIn",
                "hideMethod": "fadeOut"
            }
            toastr.warning('No report was found');
            return;
        }

        $('.report-modal-body').html(studyReport);
        $('#reportModal').modal('show');
    }

    function hideStudyReport() {
        $('#reportModal').modal('hide');

    }
    function addKeyBindings() {
        $(document).keyup(function (e) {

            if (e.which == 27){
                hideStudyReport();
            } else if(e.which == 82) {
                showStudyReport();
            }

            e.preventDefault(); // prevent the default action (scroll / move caret)
        });
    }


    function prepareScanStack(seriesUid, seriesData, stackId) {
        var stack = {
            seriesUid: seriesUid,
            seriesId: aidocViewer.services.ScanService.getSeriesId(seriesUid),
            stackId: stackId,
            imageIds: [],
            currentImageIdIndex: 0,
            type: 'scan',
            plane: seriesData.plane
        };

        for (var i = 1; i <= seriesData.slices; i++) {
            stack.imageIds.push(aidocViewer.utils.imageIdUtils.generate(seriesUid, i));
        }

        return stack;
    }

    function prepareFindingsStack(findings, stackId) {
        var stack = {
            stackId: stackId,
            imageIds: [],
            currentImageIdIndex: 0,
            type: 'findings'
        };

        aidocViewer.utils.finding.prepareFindingsStack(stack, findings);

        return stack;
    }

}
