var templateCache = {};

templateCache["templates/add_user.html"] = "<div id=\"admin\" class=\"admin-view\">\n" +
   "    <!-- Nav bar -->\n" +
   "    <nav class=\"myNav navbar navbar-default\" role=\"navigation\">\n" +
   "        <div class=\"container-fluid\">\n" +
   "            <ul class=\"nav navbar-nav pull-left\">\n" +
   "                <li>\n" +
   "                    <a href=\"/\" class=\"back-to-worklist-link\"><button class=\"btn btn-lg back-to-worklist-link\" title=\"Back\"><span class=\"fa fa-list\"></span></button>\n" +
   "</a>\n" +
   "                </li>\n" +
   "                <li>\n" +
   "                    <div class=\"navbar-user-name\"></div>\n" +
   "                </li>\n" +
   "            </ul>\n" +
   "            <ul class=\"nav navbar-nav pull-right\">\n" +
   "                <li>\n" +
   "                    <a href class=\"call-support-link\"><i class=\"glyphicon glyphicon-phone-alt\" aria-hidden=\"true\"></i>\n" +
   "                        Support</a>\n" +
   "                </li>\n" +
   "                <li>\n" +
   "                    <a href=\"/logout\" class=\"logout-link\"><span class=\"glyphicon glyphicon-log-out\"></span> Logout</a>\n" +
   "                </li>\n" +
   "            </ul>\n" +
   "        </div>\n" +
   "    </nav>\n" +
   "\n" +
   "    <div class=\"admin-sidebar-wrapper\">\n" +
   "\n" +
   "         <!-- Sidebar -->\n" +
   "        <nav id=\"sidebar\">\n" +
   "        </nav>\n" +
   "\n" +
   "        <div class=\"admin-view-content\">\n" +
   "            <div class=\"container-fluid\">\n" +
   "\n" +
   "                <div id=\"add-user-view\" class=\"add-user-view\">\n" +
   "                    <div class=\"add-user-form-title\">\n" +
   "                        <img class=\"add-user-form-title-logo\" src=\"/static/images/add.png\">\n" +
   "                        <h1 class=\"add-user-form-title-text\">Add User</h1>\n" +
   "                    </div>\n" +
   "                    <div class=\"add-user-form-container\">\n" +
   "                        <form action=\"\" id=\"add-user-form\">\n" +
   "                            <div class=\"add-user-fields-container\">\n" +
   "                                <div class=\"form-group\">\n" +
   "                                    <label for=\"inputName\">Full Name</label>\n" +
   "                                    <input type=\"text\" class=\"add-user-form-control form-control\" id=\"inputName\" placeholder=\"Full Name\">\n" +
   "                                </div>\n" +
   "                                <div class=\"form-group\">\n" +
   "                                    <label for=\"inputUsername\">User name</label>\n" +
   "\n" +
   "                                    <input type=\"text\" class=\"add-user-form-control form-control\" id=\"inputUsername\" placeholder=\"User name\">\n" +
   "                                </div>\n" +
   "\n" +
   "                                <div class=\"form-group\">\n" +
   "                                    <label for=\"inputEmail\">Email</label>\n" +
   "\n" +
   "                                    <input type=\"text\" class=\"add-user-form-control form-control\" id=\"inputEmail\" placeholder=\"Email\">\n" +
   "                                </div>\n" +
   "\n" +
   "                                <div class=\"form-group\">\n" +
   "                                    <label for=\"inputRole\">Role</label>\n" +
   "\n" +
   "                                    <select id=\"inputRole\">\n" +
   "                                    </select>\n" +
   "                                </div>\n" +
   "                                <div class=\"form-group\">\n" +
   "                                    <label for=\"clone-data-from\">Clone worklist from</label>\n" +
   "\n" +
   "                                    <select id=\"clone-data-from\">\n" +
   "\n" +
   "                                    </select>\n" +
   "                                </div>\n" +
   "                                <div class=\"form-group\">\n" +
   "                                    <label class=\"form-check-label\">\n" +
   "                                        <input type=\"checkbox\" class=\"form-check-input\" id=\"loadFindingFiles\" checked>\n" +
   "                                        Load-data action - will load finding files\n" +
   "                                    </label>\n" +
   "                                </div>\n" +
   "\n" +
   "                            </div>\n" +
   "                            <div class=\"add-user-form-button-container\">\n" +
   "                                <button type=\"submit\" class=\"btn btn-primary\">\n" +
   "                                    Create\n" +
   "                                </button>\n" +
   "                            </div>\n" +
   "\n" +
   "                        </form>\n" +
   "\n" +
   "\n" +
   "                    </div>\n" +
   "                </div>\n" +
   "                <div class=\"container-fluid\">\n" +
   "                    <textarea id=\"txt-user-added\" rows=\"5\" cols=\"100\"  style=\"display:none;\" disabled></textarea>\n" +
   "                </div>\n" +
   "\n" +
   "            </div>\n" +
   "\n" +
   "\n" +
   "        </div>\n" +
   "\n" +
   "    </div>\n" +
   "\n" +
   "    <div class=\"aidoc-footer-bar\"></div>\n" +
   "</div>\n" +
   "\n" +
   "\n" +
   "\n" +
   "";

templateCache["templates/admin.html"] = "<div id=\"admin\" class=\"admin-view\">\n" +
   "    <!-- Nav bar -->\n" +
   "    <nav class=\"myNav navbar navbar-default\" role=\"navigation\">\n" +
   "        <div class=\"container-fluid\">\n" +
   "            <ul class=\"nav navbar-nav pull-left\">\n" +
   "                <li>\n" +
   "                      <a href=\"/\" class=\"back-to-worklist-link\"><<span class=\"fa fa-list\"></span>\n" +
   "</a>               </li>\n" +
   "                <li>\n" +
   "                    <div class=\"navbar-user-name\"></div>\n" +
   "                </li>\n" +
   "            </ul>\n" +
   "            <ul class=\"nav navbar-nav pull-right\">\n" +
   "                <li>\n" +
   "                    <a href=\"/logout\" class=\"logout-link\"><span class=\"glyphicon glyphicon-log-out\"></span> Logout</a>\n" +
   "                </li>\n" +
   "            </ul>\n" +
   "        </div>\n" +
   "    </nav>\n" +
   "\n" +
   "    <div class=\"admin-sidebar-wrapper\">\n" +
   "\n" +
   "       <!-- Sidebar -->\n" +
   "        <div id=\"sidebar\"/>\n" +
   "\n" +
   "\n" +
   "        <div class=\"admin-view-content\"></div>\n" +
   "\n" +
   "    </div>\n" +
   "\n" +
   "    <div class=\"aidoc-footer-bar\"></div>\n" +
   "</div>\n" +
   "";

templateCache["templates/findingActions.html"] = "<div class=\"finding-actions-popup\">\n" +
   "    <div class=\"finding-actions-btn-container\">\n" +
   "        <a href=\"#\" class=\"btn finding-action-btn relocate-action-btn\" title=\"Relocate\">\n" +
   "            <i class=\"fa fa-arrows-alt\" aria-hidden=\"true\"></i>\n" +
   "        </a>\n" +
   "        <a href=\"#\" class=\"btn finding-action-btn set-target-point-action-btn\" title=\"Set target point\">\n" +
   "            <i class=\"fa fa-bullseye\" aria-hidden=\"true\"></i>\n" +
   "        </a>\n" +
   "        <a href=\"#\" class=\"btn finding-action-btn reset-finding-action-btn\" title=\"Reset\">\n" +
   "            <i class=\"fa fa-undo\" aria-hidden=\"true\"></i>\n" +
   "        </a>\n" +
   "    </div>\n" +
   "    <div class=\"clearfix finding-actions-comments-panel\">\n" +
   "        <textarea class=\"finding-actions-comments\" rows=\"4\" placeholder=\"Add comment...\"\n" +
   "                  autocomplete=\"off\" autocorrect=\"off\" autocapitalize=\"off\" spellcheck=\"false\">\n" +
   "        </textarea>\n" +
   "        <button type=\"button\" class=\"btn btn-default finding-action-btn delete-action-btn\" title=\"Delete\">\n" +
   "            <i class=\"fa fa-trash\" aria-hidden=\"true\"></i>\n" +
   "        </button>\n" +
   "        <button type=\"button\" class=\"btn btn-primary finding-actions-popup-done-button\">DONE</button>\n" +
   "    </div>\n" +
   "</div>\n" +
   "";

templateCache["templates/login.html"] = "<div id=\"login-view\" class=\"login-view\">\n" +
   "    <div class=\"login-form-title\">\n" +
   "        <img class=\"login-form-title-logo\" src=\"/static/images/logo-white.png\">\n" +
   "        <h1 class=\"login-form-title-text\">Validation Platform</h1>\n" +
   "    </div>\n" +
   "    <div class=\"login-form-container\">\n" +
   "        <form action=\"\" id=\"login-form\">\n" +
   "            <div class=\"login-fields-container\">\n" +
   "                <div class=\"form-group\">\n" +
   "                    <input type=\"text\" class=\"form-control\" id=\"inputUsername\" placeholder=\"User name\">\n" +
   "                </div>\n" +
   "                <div class=\"form-group\">\n" +
   "                    <input type=\"password\" class=\"form-control\" id=\"inputPassword\" placeholder=\"Password\">\n" +
   "                </div>\n" +
   "            </div>\n" +
   "            <div class=\"login-form-button-container\">\n" +
   "                <button class=\"login-form-submit-button\" type=\"submit\" class=\"btn btn-primary\">Login</button>\n" +
   "            </div>\n" +
   "            <div class=\"login-support-container hidden\">\n" +
   "                Need assistance? Call our support team at: <span class=\"login-support-phone-number\"></span>\n" +
   "            </div>\n" +
   "            <div class=\"quit-app-link-container hidden\">\n" +
   "                Done? <a href class=\"quit-app-link\">Click here to quit</a>\n" +
   "            </div>\n" +
   "        </form>\n" +
   "    </div>\n" +
   "</div>\n" +
   "";

templateCache["templates/metrics.html"] = "<div id=\"admin\" class=\"admin-view\">\n" +
   "    <!-- Nav bar -->\n" +
   "    <nav class=\"myNav navbar navbar-default\" role=\"navigation\">\n" +
   "        <div class=\"container-fluid\">\n" +
   "            <ul class=\"nav navbar-nav pull-left\">\n" +
   "                <li>\n" +
   "                    <a href=\"/\" class=\"back-to-worklist-link\"><span class=\"fa fa-list\"></span></a>\n" +
   "                </li>\n" +
   "                <li>\n" +
   "                    <div class=\"navbar-user-name\"></div>\n" +
   "                </li>\n" +
   "            </ul>\n" +
   "            <ul class=\"nav navbar-nav pull-right\">\n" +
   "\n" +
   "                <li>\n" +
   "                    <a href=\"/logout\" class=\"logout-link\"><span class=\"glyphicon glyphicon-log-out\"></span> Logout</a>\n" +
   "                </li>\n" +
   "            </ul>\n" +
   "        </div>\n" +
   "    </nav>\n" +
   "\n" +
   "    <div class=\"admin-sidebar-wrapper\">\n" +
   "\n" +
   "        <!-- Sidebar -->\n" +
   "        <div id=\"sidebar\"/>\n" +
   "\n" +
   "\n" +
   "        <div class=\"metrics-table-container\">\n" +
   "            <h3>Metrics</h3>\n" +
   "            <table class=\"table metrics-table\">\n" +
   "                <thead>\n" +
   "                <tr>\n" +
   "                    <th>User</th>\n" +
   "                    <th># of scans</th>\n" +
   "                    <th>Finding TP</th>\n" +
   "                    <th>Finding FP</th>\n" +
   "                    <th>Scan TP</th>\n" +
   "                    <th>Scan FP</th>\n" +
   "                    <th>Scan TN</th>\n" +
   "                    <th>Scan FN</th>\n" +
   "                    <th>Finding precision</th>\n" +
   "                    <th>Scan sensitivity</th>\n" +
   "                    <th>Scan specificity</th>\n" +
   "                    <th>Scan accuracy</th>\n" +
   "                </tr>\n" +
   "                </thead>\n" +
   "                <tbody>\n" +
   "                </tbody>\n" +
   "            </table>\n" +
   "        </div>\n" +
   "\n" +
   "\n" +
   "    </div>\n" +
   "\n" +
   "    <div class=\"aidoc-footer-bar\"></div>\n" +
   "</div>\n" +
   "\n" +
   "\n" +
   "";

templateCache["templates/scan.html"] = "<div id=\"scan-view\" class=\"scan-view\">\n" +
   "</div>\n" +
   "";

templateCache["templates/seriesViewer.html"] = "<div id=\"seriesViewerTemplate\" class=\"series-viewer\">\n" +
   "\n" +
   "    <nav class=\"navbar navbar-default\" role=\"navigation\">\n" +
   "        <div class=\"container-fluid\">\n" +
   "            <ul class=\"nav navbar-nav navigation-links pull-left\">\n" +
   "\n" +
   "                <li>\n" +
   "                   <button class=\"btn btn-lg back-to-worklist-link\" title=\"Back\"><span class=\"fa fa-list\"></span></button>\n" +
   "                </li>\n" +
   "                <li>\n" +
   "                    <button class=\"btn btn-lg prev-scan-link\" title=\"Prev\"><span class=\"fa fa-chevron-left\"></span></button>\n" +
   "                </li>\n" +
   "                <li>\n" +
   "                    <button class=\"btn btn-lg next-scan-link\" title=\"Next\"><span class=\"fa fa-chevron-right\"></span></button>\n" +
   "                </li>\n" +
   "                <li>\n" +
   "                    <div class=\"aidoc-logo-floating\">\n" +
   "                        <img src=\"/static/images/logo-white.png\">\n" +
   "                    </div>\n" +
   "                </li>\n" +
   "                <li>\n" +
   "                    <div class=\"navbar-user-name\" hidden></div>\n" +
   "                </li>\n" +
   "            </ul>\n" +
   "\n" +
   "            <div class=\"center-content\">\n" +
   "                <span class=\"scan-patient-name\" title=\"Patient name\"></span>\n" +
   "                <span class=\"patient-location-name\" title=\"Patient location\"></span>\n" +
   "                <span class=\"series-uid\" title=\"Series UID\"></span>\n" +
   "                <span class=\"accession-number\" title=\"Accession number\"></span>\n" +
   "            </div>\n" +
   "            <ul class=\"nav navbar-nav pull-right\">\n" +
   "                <li class=\"call-support-link-container hidden\">\n" +
   "                    <a href class=\"call-support-link\"><i class=\"glyphicon glyphicon-phone-alt\" aria-hidden=\"true\"></i> Support</a>\n" +
   "                </li>\n" +
   "                <li>\n" +
   "                    <a href=\"/logout\" class=\"logout-link\"><span class=\"glyphicon glyphicon-log-out\"></span> Logout</a>\n" +
   "                </li>\n" +
   "            </ul>\n" +
   "        </div>\n" +
   "    </nav>\n" +
   "\n" +
   "    <div class=\"seriesContainer\">\n" +
   "        <div class=\"seriesRow row\" style=\"height:100%\">\n" +
   "\n" +
   "            <!-- Viewer -->\n" +
   "            <div class=\"viewer\">\n" +
   "                <!-- Toolbar -->\n" +
   "                <div class=\"clearfix viewer-toolbar\">\n" +
   "                    <div class=\"btn-group toolbar-btn-group pull-left scan-state-modify-toolbar\">\n" +
   "                        <!-- Undo -->\n" +
   "                        <button type=\"button\" class=\"btn btn-sm btn-default undo-btn\" disabled=\"disabled\" data-toggle=\"tooltip\" data-placement=\"bottom\" title=\"Undo\"><span class=\"fa fa-undo\"></span></button>\n" +
   "                        <!-- Redo -->\n" +
   "                        <button type=\"button\" class=\"btn btn-sm btn-default redo-btn\" disabled=\"disabled\" data-toggle=\"tooltip\" data-placement=\"bottom\" title=\"Redo\"><span class=\"fa fa-repeat\"></span></button>\n" +
   "                        <!-- Reset scan -->\n" +
   "                        <button type=\"button\" class=\"btn btn-sm btn-default reset-scan-btn\" data-toggle=\"tooltip\" data-placement=\"bottom\" title=\"Reset scan to initial state\"><span class=\"glyphicon glyphicon-erase\"></span></button>\n" +
   "                    </div>\n" +
   "                    <div class=\"btn-group toolbar-btn-group pull-right add-finding-btn-group\">\n" +
   "                        <!-- Add finding -->\n" +
   "                        <button type=\"button\" class=\"btn btn-sm btn-default add-finding-btn\" data-toggle=\"tooltip\" data-placement=\"bottom\" title=\"Add a new finding\">\n" +
   "                            <img src=\"static/images/add-anomaly-16.png\" class=\"toolbar-icon\">\n" +
   "                        </button>\n" +
   "                    </div>\n" +
   "                    <div class=\"btn-group toolbar-btn-group pull-right\">\n" +
   "                        <!-- WW/WL -->\n" +
   "                        <button type=\"button\" class=\"btn btn-sm btn-default wwwc-btn\" data-toggle=\"tooltip\" data-placement=\"bottom\" title=\"WW/WC\">\n" +
   "                            <img src=\"static/images/toolbar-ww-wc.png\" class=\"toolbar-icon\">\n" +
   "                        </button>\n" +
   "                        <!-- Zoom -->\n" +
   "                        <button type=\"button\" class=\"btn btn-sm btn-default zoom-btn\" data-toggle=\"tooltip\" data-placement=\"bottom\" title=\"Zoom\">\n" +
   "                            <img src=\"static/images/toolbar-zoom.png\" class=\"toolbar-icon\">\n" +
   "                        </button>\n" +
   "                        <!-- Pan -->\n" +
   "                        <button type=\"button\" class=\"btn btn-sm btn-default pan-btn\" data-toggle=\"tooltip\" data-placement=\"bottom\" title=\"Pan\">\n" +
   "                            <img src=\"static/images/toolbar-pan.png\" class=\"toolbar-icon\">\n" +
   "                        </button>\n" +
   "                        <!-- Stack scroll -->\n" +
   "                        <button type=\"button\" class=\"btn btn-sm btn-default stack-scroll-btn\" data-toggle=\"tooltip\" data-placement=\"bottom\" title=\"Stack Scroll\"><span class=\"fa fa-bars\"></span></button>\n" +
   "                        <!-- Pixel probe -->\n" +
   "                        <!--<button type=\"button\" class=\"btn btn-sm btn-default pixel-probe-btn\" data-toggle=\"tooltip\" data-placement=\"bottom\" title=\"Pixel Probe\"><span class=\"fa fa-dot-circle-o\"></span></button>-->\n" +
   "                        <!--<span class=\"dropdown\">-->\n" +
   "                            <!--<button type=\"button\" class=\"btn btn-sm btn-default dropdown-toggle\" data-toggle=\"dropdown\" aria-expanded=\"false\" data-placement=\"top\" title=\"Layout\"><span class=\"fa fa-th-large\"></span></button>-->\n" +
   "                            <!--<ul class=\"dropdown-menu choose-layout\" role=\"menu\">-->\n" +
   "                                <!--<li><a href>1x1</a></li>-->\n" +
   "                                <!--<li><a href>2x1</a></li>-->\n" +
   "                                <!--<li><a href>1x2</a></li>-->\n" +
   "                                <!--<li><a href>2x2</a></li>-->\n" +
   "                            <!--</ul>-->\n" +
   "                        <!--</span>-->\n" +
   "                        <!-- Key slice indicator -->\n" +
   "                        <!--<button type=\"button\" class=\"btn btn-sm btn-default key-slice-indicator-btn push-btn active\" data-toggle=\"tooltip\" data-placement=\"bottom\" title=\"Key slice indicator\"><span class=\"fa fa-key\"></span></button>-->\n" +
   "                        <!-- Show findings only on key slices -->\n" +
   "                        <!--<button type=\"button\" class=\"btn btn-sm btn-default show-findings-on-key-slice-btn push-btn active\" data-toggle=\"tooltip\" data-placement=\"bottom\" title=\"Show findings only on key slices\"><span class=\"fa fa-bullseye\"></span></button>-->\n" +
   "                    </div>\n" +
   "                </div>\n" +
   "\n" +
   "                <div class=\"image-viewer-container\">\n" +
   "                    <!-- Viewer -->\n" +
   "                    <div class=\"imageViewer\">\n" +
   "                    </div>\n" +
   "                </div>\n" +
   "            </div>\n" +
   "\n" +
   "            <!-- Toolbox -->\n" +
   "            <div class=\"toolbox-container\">\n" +
   "                <div class=\"panel panel-default\">\n" +
   "                    <div class=\"panel-heading\">\n" +
   "                        <h3 class=\"panel-title\">Findings</h3>\n" +
   "                        <!--<a href class=\"toolbox-header-button undock-toolbox-button\" title=\"Undock\"><i class=\"fa fa-unlock\" aria-hidden=\"true\"></i></a>-->\n" +
   "                    </div>\n" +
   "                    <div class=\"list-group findings-list-box aidoc-findings-list-box\">\n" +
   "                    </div>\n" +
   "                </div>\n" +
   "\n" +
   "                <div class=\"panel panel-default user-findings-panel\">\n" +
   "                    <div class=\"panel-heading\">\n" +
   "                        <h3 class=\"panel-title\">My Findings</h3>\n" +
   "                    </div>\n" +
   "                    <div class=\"list-group findings-list-box user-findings-list-box\">\n" +
   "                    </div>\n" +
   "                </div>\n" +
   "\n" +
   "                <div class=\"scan-action-bar\">\n" +
   "                    <div class=\"finalize-scan-panel\">\n" +
   "                           <button class=\"btn btn-primary btn-lg finalize-scan-button finalize-scan-button-as-positive\">Finalize as positive</button>\n" +
   "                           <button class=\"btn btn-primary btn-lg finalize-scan-button finalize-scan-button-as-negative\">Finalize as negative</button>\n" +
   "                    </div>\n" +
   "                    <div class=\"finalize-incomplete-panel\">\n" +
   "                        <p>Do you want to continue reading or exit and save as a draft?</p>\n" +
   "                        <button class=\"btn btn-primary btn-lg cancel-finalize-button\">Continue</button>\n" +
   "                        <button class=\"btn btn-default btn-lg save-as-draft-button\">Save as draft</button>\n" +
   "                    </div>\n" +
   "                </div>\n" +
   "            </div>\n" +
   "        </div>\n" +
   "        <div style=\"clear:both;\"></div>\n" +
   "    </div>\n" +
   "    <div class=\"disclaimer-footer-bar\"><h3>The software display is for demonstration purposes only</h3></div>\n" +
   "</div>\n" +
   "";

templateCache["templates/upload.html"] = "<div id=\"admin\" class=\"admin-view\">\n" +
   "    <!-- Nav bar -->\n" +
   "    <nav class=\"myNav navbar navbar-default\" role=\"navigation\">\n" +
   "        <div class=\"container-fluid\">\n" +
   "            <ul class=\"nav navbar-nav pull-left\">\n" +
   "                <li>\n" +
   "                    <a href=\"/\" class=\"back-to-worklist-link\"><span class=\"fa fa-list\"></span></a>\n" +
   "                </li>\n" +
   "                <li>\n" +
   "                    <div class=\"navbar-user-name\"></div>\n" +
   "                </li>\n" +
   "            </ul>\n" +
   "            <ul class=\"nav navbar-nav pull-right\">\n" +
   "                <li>\n" +
   "                    <a href=\"/logout\" class=\"logout-link\"><span class=\"glyphicon glyphicon-log-out\"></span> Logout</a>\n" +
   "                </li>\n" +
   "            </ul>\n" +
   "        </div>\n" +
   "    </nav>\n" +
   "\n" +
   "    <div class=\"admin-sidebar-wrapper\">\n" +
   "\n" +
   "        <!-- Sidebar -->\n" +
   "        <nav id=\"sidebar\">\n" +
   "        </nav>\n" +
   "\n" +
   "        <div class=\"admin-view-content\">\n" +
   "\n" +
   "            <div class=\"container-fluid\">\n" +
   "                <h2>Upload data (up to 10GB)</h2>\n" +
   "                <form action=\"\" id=\"upload-data-form\" method=post enctype=multipart/form-data>\n" +
   "                    <div>\n" +
   "                        <div class=\"form-group \">\n" +
   "                            <label for=\"fileChooser\">Scan files.</label>\n" +
   "                            <input class=\"input-group input-file\" type=file name=scanFiles multiple=\"\" id=\"fileChooser\"\n" +
   "                                   accept=\".mat\">\n" +
   "\n" +
   "                        </div>\n" +
   "                        <div class=\"form-group \">\n" +
   "                            <label for=\"fileChooser\">DICOM directories.</label>\n" +
   "                            <input class=\"input-group input-file\" type=file name=dicomFiles id=\"dicomFileChooser\"\n" +
   "                                   accept=\".dcm\" webkitdirectory=\"\" directory=\"\"  multiple=\"\">\n" +
   "\n" +
   "                        </div>\n" +
   "\n" +
   "                        <div class=\"form-group \">\n" +
   "                            <label for=\"findingsFileChooser\">Findings files. </label>\n" +
   "                            <input class=\"input-group input-file\" type=file name=findingFiles multiple=\"\"\n" +
   "                                   id=\"findingsFileChooser\" accept=\".json\">\n" +
   "                        </div>\n" +
   "\n" +
   "                        <div class=\"form-group \">\n" +
   "                            <label for=\"worklistFileChooser\">User worklist files. Filename should be the\n" +
   "                                username</label>\n" +
   "                            <input class=\"input-group input-file\" type=file name=worklistFiles multiple=\"\"\n" +
   "                                   id=\"worklistFileChooser\">\n" +
   "                        </div>\n" +
   "\n" +
   "                        <div class=\"form-check\">\n" +
   "                            <label class=\"form-check-label\">\n" +
   "                                <input type=\"checkbox\" class=\"form-check-input\" name=\"overwrite\">\n" +
   "                                Overwrite DB\n" +
   "                            </label>\n" +
   "                        </div>\n" +
   "\n" +
   "                        <div class=\"form-group \">\n" +
   "                            <button id=\"uploadSubmitBtn\" type=\"submit\" class=\"btn btn-primary\">Upload</button>\n" +
   "\n" +
   "                        </div>\n" +
   "                    </div>\n" +
   "\n" +
   "                </form>\n" +
   "\n" +
   "                <div id=\"uploadProgressBar\" hidden>\n" +
   "                    <button class=\"abort btn btn-danger\" type=\"submit\">Abort</button>\n" +
   "                    <div id=\"myProgress\">\n" +
   "                        <div id=\"myBar\" class=\"percent\">0</div>\n" +
   "                    </div>\n" +
   "                    <div class=\"status\"></div>\n" +
   "\n" +
   "                </div>\n" +
   "\n" +
   "                <textarea id=\"txt-data-uploaded\" rows=\"5\" cols=\"100\" hidden disabled></textarea>\n" +
   "\n" +
   "            </div>\n" +
   "        </div>\n" +
   "    </div>\n" +
   "\n" +
   "    <div class=\"aidoc-footer-bar\"></div>\n" +
   "</div>\n" +
   "\n" +
   "";

templateCache["templates/users.html"] = "<div id=\"admin\" class=\"admin-view\">\n" +
   "    <!-- Nav bar -->\n" +
   "    <nav class=\"myNav navbar navbar-default\" role=\"navigation\">\n" +
   "        <div class=\"container-fluid\">\n" +
   "            <ul class=\"nav navbar-nav pull-left\">\n" +
   "                <li>\n" +
   "                    <a href=\"/\" class=\"back-to-worklist-link\"><span class=\"fa fa-list\"></span></a>\n" +
   "                </li>\n" +
   "                <li>\n" +
   "                    <div class=\"navbar-user-name\"></div>\n" +
   "                </li>\n" +
   "            </ul>\n" +
   "            <ul class=\"nav navbar-nav pull-right\">\n" +
   "                <li>\n" +
   "                    <a href=\"/logout\" class=\"logout-link\"><span class=\"glyphicon glyphicon-log-out\"></span> Logout</a>\n" +
   "                </li>\n" +
   "            </ul>\n" +
   "        </div>\n" +
   "    </nav>\n" +
   "\n" +
   "    <div class=\"admin-sidebar-wrapper\">\n" +
   "\n" +
   "        <!-- Sidebar -->\n" +
   "        <nav id=\"sidebar\">\n" +
   "\n" +
   "\n" +
   "        </nav>\n" +
   "\n" +
   "\n" +
   "        <div class=\"admin-view-content\">\n" +
   "            <div class=\"container-fluid\" s>\n" +
   "\n" +
   "                <nav class=\"navbar navbar-default\" role=\"navigation\" id=\"users-nav-bar\">\n" +
   "                    <div class=\"container-fluid\">\n" +
   "\n" +
   "                        <ul class=\"nav navbar-nav\">\n" +
   "                            <li>\n" +
   "                                <a href=\"/admin/users/add-user\"><img\n" +
   "                                        src=\"static/images/add.png\" class=\"toolbar-icon\"></a>\n" +
   "                            </li>\n" +
   "\n" +
   "                        </ul>\n" +
   "                    </div>\n" +
   "                </nav>\n" +
   "\n" +
   "                <div class=\"users-table-container\">\n" +
   "                    <table class=\"table table-hover users-table\" id=\"users-table\">\n" +
   "                        <thead>\n" +
   "                        <tr>\n" +
   "                            <th> Username</th>\n" +
   "                            <th> Name</th>\n" +
   "                            <th> Email </th>\n" +
   "                            <th> Role</th>\n" +
   "                            <th> Created On</th>\n" +
   "                            <th> Last Login</th>\n" +
   "                            <th> Logged In From</th>\n" +
   "                            <th> Actions</th>\n" +
   "                        </tr>\n" +
   "                        </thead>\n" +
   "                        <tbody>\n" +
   "                        </tbody>\n" +
   "                    </table>\n" +
   "                </div>\n" +
   "            </div>\n" +
   "\n" +
   "\n" +
   "        </div>\n" +
   "\n" +
   "    </div>\n" +
   "\n" +
   "    <div class=\"aidoc-footer-bar\"></div>\n" +
   "</div>\n" +
   "";

templateCache["templates/viewport.html"] = "<div class=\"viewportWrapper\"\n" +
   "     oncontextmenu=\"return false\"\n" +
   "     class='cornerstone-enabled-image'\n" +
   "     unselectable='on'\n" +
   "     onselectstart='return false;'\n" +
   "     onclick='return false;'>\n" +
   "    <!-- Viewport -->\n" +
   "    <div class=\"viewport\"></div>\n" +
   "\n" +
   "    <!-- Overlays -->\n" +
   "    <div class=\"overlay\" style=\"top:0px; left:9px\">\n" +
   "        <!--<div>Patient Name</div>-->\n" +
   "        <!--<div>Patient Id</div>-->\n" +
   "    </div>\n" +
   "\n" +
   "    <div class=\"overlay\" style=\"top:0px; right:9px\">\n" +
   "        <!--<div>Study Description</div>-->\n" +
   "        <!--<div>Study Date</div>-->\n" +
   "    </div>\n" +
   "\n" +
   "    <div class=\"overlay overlay-bottom-left\" style=\"bottom:16px; left:9px\">\n" +
   "        <div class=\"slice-pixel-data\"></div>\n" +
   "        <div class=\"scan-slice-number\"></div>\n" +
   "        <div class=\"currentImageAndTotalImages\">Image #:</div>\n" +
   "    </div>\n" +
   "\n" +
   "    <div class=\"overlay overlay-bottom-center\" style=\"bottom:16px\">\n" +
   "        <div class=\"series-type\"></div>\n" +
   "    </div>\n" +
   "\n" +
   "    <div class=\"overlay overlay-bottom-right\" style=\"bottom:16px; right:9px\">\n" +
   "        <div class=\"image-viewport-zoom\">Zoom:</div>\n" +
   "        <div class=\"image-viewport-windowing\">WW/WC:</div>\n" +
   "    </div>\n" +
   "</div>\n" +
   "";

templateCache["templates/worklist.html"] = "<div id=\"workList\" class=\"worklist-view\">\n" +
   "    <!-- Nav bar -->\n" +
   "    <nav class=\"myNav navbar navbar-default\" role=\"navigation\">\n" +
   "        <div class=\"container-fluid\">\n" +
   "            <ul class=\"nav navbar-nav pull-left\">\n" +
   "                <li>\n" +
   "                    <div class=\"aidoc-logo-floating\">\n" +
   "                        <img src=\"/static/images/logo-white.png\">\n" +
   "                    </div>\n" +
   "                </li>\n" +
   "                <li>\n" +
   "                    <div class=\"navbar-user-name\"></div>\n" +
   "                </li>\n" +
   "            </ul>\n" +
   "            <ul class=\"nav navbar-nav pull-right\">\n" +
   "                <li class=\"admin-link-container hidden\">\n" +
   "                    <a href=\"/admin\" class=\"admin-link\"><i class=\"fa fa-user-secret\" aria-hidden=\"true\"></i> Admin</a>\n" +
   "                </li>\n" +
   "                <li class=\"call-support-link-container hidden\">\n" +
   "                    <a href class=\"call-support-link\"><i class=\"glyphicon glyphicon-phone-alt\" aria-hidden=\"true\"></i> Support</a>\n" +
   "                </li>\n" +
   "                <li>\n" +
   "                    <a href=\"/logout\" class=\"logout-link\"><span class=\"glyphicon glyphicon-log-out\"></span> Logout</a>\n" +
   "                </li>\n" +
   "                <li class=\"quit-app-link-container hidden\">\n" +
   "                    <a href class=\"quit-app-link\"><span class=\"fa fa-power-off\"></span> Quit</a>\n" +
   "                </li>\n" +
   "            </ul>\n" +
   "        </div>\n" +
   "    </nav>\n" +
   "\n" +
   "    <div class=\"scrollable-container\">\n" +
   "        <div class=\"row\">\n" +
   "            <div class=\"clearfix worklist-table-title\">\n" +
   "                <h1 class=\"worklist-title\"></h1>\n" +
   "                <div class=\"worklist-table-filters\">\n" +
   "                    <a href class=\"worklist-table-filter worklist-table-filter-all\">\n" +
   "                        All<span class=\"badge all-counter\"></span>\n" +
   "                    </a>\n" +
   "                    <a href class=\"worklist-table-filter worklist-table-filter-pending selected\">\n" +
   "                        Pending<span class=\"badge pending-counter\"></span>\n" +
   "                    </a>\n" +
   "                </div>\n" +
   "                <div class=\"worklist-table-total-badge\" hidden><h3>Total <span class=\"badge all-counter\"></span></h3></div>\n" +
   "            </div>\n" +
   "            <table class=\"col-md-12 table table-striped worklist-table\">\n" +
   "                <thead>\n" +
   "                <tr class=\"worklist-table-header\">\n" +
   "                    <th></th>\n" +
   "                    <th>Patient Name</th>\n" +
   "                    <th>Patient ID</th>\n" +
   "                    <th>Study Time</th>\n" +
   "                    <th>Type</th>\n" +
   "                    <th>Modality</th>\n" +
   "                    <th class=\"work-item-demo-col\">Location</th>\n" +
   "                    <th class=\"work-item-demo-col\">Priority</th>\n" +
   "                    <th class=\"work-item-demo-col\">AI Findings</th>\n" +
   "                    <th class=\"work-item-extra-col\">Accession Number</th>\n" +
   "                    <th class=\"work-item-extra-col\">Status</th>\n" +
   "                    <th class=\"work-item-favorite-column work-item-extra-col\"><i class=\"fa fa-star-o\" aria-hidden=\"true\"></i></th>\n" +
   "\n" +
   "                </tr>\n" +
   "                </thead>\n" +
   "\n" +
   "                <tbody id=\"workListData\">\n" +
   "                <!-- Table rows get populated from the JSON workList manifest -->\n" +
   "                </tbody>\n" +
   "            </table>\n" +
   "        </div>\n" +
   "    </div>\n" +
   "\n" +
   "\n" +
   "    <div class=\"disclaimer-footer-bar\"><h3>The software display is for demonstration purposes only</h3></div>\n" +
   "</div>\n" +
   "";
