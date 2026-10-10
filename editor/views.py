import os
import subprocess
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, FileResponse
from django.conf import settings
from .models import Video
from .forms import VideoUploadForm, VideoEditForm

def home(request):
    videos = Video.objects.all().order_by('-created_at')
    return render(request, 'editor/home.html', {'videos': videos})

def upload_video(request):
    if request.method == 'POST':
        form = VideoUploadForm(request.POST, request.FILES)
        if form.is_valid():
            video = form.save()
            return redirect('process_video', pk=video.pk)
    else:
        form = VideoUploadForm()
    return render(request, 'editor/upload.html', {'form': form})

def process_video(request, pk):
    video = get_object_or_404(Video, pk=pk)
    all_videos = Video.objects.exclude(pk=pk)
    
    if request.method == 'POST':
        action = request.POST.get('action')
        output_path = None
        cmd = None
        
        input_path = video.original_file.path
        filename = os.path.basename(input_path)
        name, ext = os.path.splitext(filename)
        
        output_dir = os.path.join(settings.MEDIA_ROOT, 'videos', 'processed')
        os.makedirs(output_dir, exist_ok=True)

        if action == 'trim':
            start = request.POST.get('start', '00:00:00')
            duration = request.POST.get('duration', '00:00:30')
            output_filename = f"{name}_trimmed{ext}"
            output_path = os.path.join(output_dir, output_filename)
            cmd = ['ffmpeg', '-i', input_path, '-ss', start, '-t', duration, '-c', 'copy', output_path]

        elif action == 'add_text':
            text = request.POST.get('text', 'Grok Video Editor')
            output_filename = f"{name}_text{ext}"
            output_path = os.path.join(output_dir, output_filename)
            cmd = ['ffmpeg', '-i', input_path, '-vf', 
                   f"drawtext=text='{text}':fontcolor=white:fontsize=48:x=(w-text_w)/2:y=h-th-50",
                   '-codec:a', 'copy', output_path]

        elif action == 'thumbnail':
            output_filename = f"{name}_thumb.jpg"
            output_path = os.path.join(output_dir, output_filename)
            cmd = ['ffmpeg', '-i', input_path, '-ss', '00:00:05', '-vframes', '1', output_path]

        elif action == 'speed':
            speed = float(request.POST.get('speed', 1.0))
            output_filename = f"{name}_speed{speed}x{ext}"
            output_path = os.path.join(output_dir, output_filename)
            if abs(speed - 1.0) < 0.01:
                cmd = ['ffmpeg', '-i', input_path, '-c', 'copy', output_path]
            else:
                cmd = ['ffmpeg', '-i', input_path, '-filter_complex',
                       f"[0:v]setpts={1/speed}*PTS[v];[0:a]atempo={speed}[a]",
                       '-map', '[v]', '-map', '[a]', '-c:v', 'libx264', '-c:a', 'aac', output_path]

        elif action == 'merge':
            second_pk = request.POST.get('second_video')
            if second_pk:
                second_video = get_object_or_404(Video, pk=second_pk)
                second_path = second_video.original_file.path
                output_filename = f"{name}_merged{ext}"
                output_path = os.path.join(output_dir, output_filename)
                
                list_path = os.path.join(output_dir, 'concat_list.txt')
                with open(list_path, 'w') as f:
                    f.write(f"file '{input_path}'\nfile '{second_path}'\n")
                
                cmd = ['ffmpeg', '-f', 'concat', '-safe', '0', '-i', list_path, '-c', 'copy', output_path]

        if cmd and output_path:
            try:
                subprocess.run(cmd, check=True, capture_output=True, text=True)
                video.processed_file = f'videos/processed/{os.path.basename(output_path)}'
                video.save()
            except subprocess.CalledProcessError as e:
                return HttpResponse(f"FFmpeg Error: {e.stderr}", status=500)
        
        return redirect('home')
    
    return render(request, 'editor/process.html', {
        'video': video,
        'all_videos': all_videos
    })

def _delete_file_if_exists(file_field):
    """Remove the physical file from disk if it exists."""
    if file_field and file_field.name:
        try:
            path = file_field.path
            if os.path.isfile(path):
                os.remove(path)
        except Exception:
            pass


def edit_video(request, pk):
    video = get_object_or_404(Video, pk=pk)
    if request.method == 'POST':
        form = VideoEditForm(request.POST, request.FILES, instance=video)
        if form.is_valid():
            old_file = video.original_file
            video = form.save(commit=False)
            video.save()
            # Remove the old file from disk if a new file was uploaded
            if 'original_file' in form.changed_data and old_file:
                _delete_file_if_exists(old_file)
            # Redirect to home 
            return redirect('home')
    else:
        form = VideoEditForm(instance=video)
    return render(request, 'editor/edit.html', {
        'video': video,
        'form': form
    })

def delete_video(request, pk):
    video = get_object_or_404(Video, pk=pk)

    if request.method == 'POST':
        _delete_file_if_exists(video.original_file)
        _delete_file_if_exists(video.processed_file)
        video.delete()
        return redirect('home')

    return render(request, 'editor/delete_confirm.html', {'video': video})

def download_file(request, filename):
    file_path = os.path.join(settings.MEDIA_ROOT, 'videos', 'processed', filename)
    if os.path.exists(file_path):
        return FileResponse(open(file_path, 'rb'), as_attachment=True)
    return HttpResponse("File not found.", status=404)