% Plot synthetic reviewer-assistant metrics exported by the Python pipeline.
% Run after: python scripts/run_synthetic_review_lab.py

resultsDir = fullfile('outputs', 'results');
figuresDir = fullfile('outputs', 'figures');
if ~exist(figuresDir, 'dir')
    mkdir(figuresDir);
end

quality = readtable(fullfile(resultsDir, 'synthetic_paper_quality_scores.csv'));
methodology = readtable(fullfile(resultsDir, 'synthetic_methodology_audit.csv'));
citations = readtable(fullfile(resultsDir, 'synthetic_citation_comparison.csv'));

figure;
histogram(quality.paper_quality_support_score);
title('Synthetic Paper Quality Support Scores');
xlabel('Support score');
ylabel('Paper count');
saveas(gcf, fullfile(figuresDir, 'matlab_quality_support_scores.png'));

figure;
histogram(methodology.methodology_risk_score);
title('Synthetic Methodology Risk Scores');
xlabel('Risk score');
ylabel('Paper count');
saveas(gcf, fullfile(figuresDir, 'matlab_methodology_risk_scores.png'));

figure;
histogram(citations.citation_coverage_score);
title('Synthetic Citation Coverage Scores');
xlabel('Coverage score');
ylabel('Paper count');
saveas(gcf, fullfile(figuresDir, 'matlab_citation_coverage_scores.png'));
