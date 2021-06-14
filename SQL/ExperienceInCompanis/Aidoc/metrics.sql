-- anatomy_yield
SELECT (sum(prediction_and_ibi_valid_anatomy_series)/ CAST(count(*) AS DECIMAL)) *100.0 AS anatomy_yield
FROM
  ( SELECT aidoc_study_uid,
           max(CAST(ib_anatomy_prediction = 1 AS INT)) AS prediction_and_ibi_valid_anatomy_series
   FROM image_based_tagging r
   JOIN series_selection ss ON (ss.series_selection_id = r.series_selection_id
                                AND r.aidoc_series_uid = ss.aidoc_series_uid)
   WHERE ss.series_selection_id = '{{series selection id}}'
     AND anatomy_ground_truth = 'P'
   GROUP BY aidoc_study_uid) AS valid_anatomy_series_statistics;


-- contrast_yield
SELECT sum(prediction_and_ibi_valid_contrast_series)/ CAST(count(*) AS DECIMAL) *100.0 AS contrast_yield
FROM
  ( SELECT aidoc_study_uid,
           max(CAST(ib_contrast_prediction = 1 AS INT)) AS prediction_and_ibi_valid_contrast_series
   FROM image_based_tagging r
   JOIN series_selection ss ON (ss.series_selection_id = r.series_selection_id
                                AND r.aidoc_series_uid = ss.aidoc_series_uid)
   WHERE ss.series_selection_id = '{{series selection id}}'
     AND contrast_ground_truth = 'P'
   GROUP BY aidoc_study_uid) AS valid_contrast_series_statistics;

-- contrast_failed
SELECT sum(ibi_valid_and_prediction_not_valid_contrast_series)/ CAST(count(*) AS DECIMAL) *100.0 AS contrast_failed
FROM
  ( SELECT aidoc_study_uid,
           max(CAST(contrast_ground_truth = 'N' AS INT)) AS ibi_valid_and_prediction_not_valid_contrast_series
   FROM image_based_tagging r
   JOIN series_selection ss ON (ss.series_selection_id = r.series_selection_id
                                AND r.aidoc_series_uid = ss.aidoc_series_uid)
   WHERE ss.series_selection_id = '{{series selection id}}'
     AND ib_contrast_prediction=1
   GROUP BY aidoc_study_uid) AS failed_contrast_series_statistics;