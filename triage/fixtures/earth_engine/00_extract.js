var col = ee.ImageCollection('MODIS/061/MOD13Q1').select('NDVI');
Export.table.toDrive({collection: col, description: 'ndvi', fileFormat: 'CSV'});
