import os
from bucketapp.bucketapp import app


port = int(os.environ.get('PORT', 5000))
app.run('', port=port)
