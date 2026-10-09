"""One native tiled-camera frame; source reviewed and AST checked, never run.

Newton 1.6.1, commit 713fecdc41caf0c9d726f5c016939f36e66e3dff.
This teaches array layout and geometry/output lifetimes. It creates no solver
or viewer and provides no runtime, calibration, image-quality or physics result.
"""

import math

import newton
from newton.sensors import SensorTiledCamera
import warp as wp


def main():
    wp.init()
    builder = newton.ModelBuilder(up_axis=newton.Axis.Z)
    builder.begin_world(label="camera_lesson")
    box = builder.add_shape_box(-1, hx=0.2, hy=0.1, hz=0.3, label="box")
    builder.end_world()
    model = builder.finalize(device="cpu")
    state = model.state()

    camera = SensorTiledCamera(model, load_textures=False)
    width, height = 64, 48
    rays = camera.utils.compute_camera_rays_pinhole(
        width, height, camera_fovs=math.radians(60.0)
    )
    # Camera looks along local -Z. The single transform is camera -> world;
    # its axes are (camera, world), unlike the output axes (world, camera).
    camera_to_world = wp.array(
        [wp.transform((0.0, 0.0, 2.0), wp.quat_identity())],
        dtype=wp.transform,
        device=model.device,
    ).reshape((1, 1))
    depth = camera.utils.create_depth_image_output(width, height)
    forward_depth = camera.utils.create_forward_depth_image_output(width, height)
    shape_id = camera.utils.create_shape_index_image_output(width, height)

    # Refit for the state being observed. In a loop, static rays and these
    # output buffers can be reused; moved geometry still needs a new refit.
    model.bvh_refit_shapes(state)
    model.bvh_refit_particles(state)
    # A completely empty render context skips the render kernel. Pre-fill all
    # channels we return; ClearData alone does not handle that branch.
    depth.fill_(-1.0)
    forward_depth.fill_(-1.0)
    shape_id.fill_(0xFFFFFFFF)
    camera.update(
        state,
        camera_to_world,
        rays,
        depth_image=depth,
        forward_depth_image=forward_depth,
        shape_index_image=shape_id,
        clear_data=SensorTiledCamera.ClearData(clear_depth=-1.0),
    )

    # Host reads/copies are explicit. Use the ID contract for validity: valid
    # wide-angle forward depth need not be positive. No geometry is classified
    # from a display colormap or from viewer pixels.
    ids = shape_id.numpy().copy()
    return {
        "source_time_s": 0.0,
        "sampling_stage": "initial_static_state_geometry",
        "image_axes": ("world", "camera", "y", "x"),
        "camera_axes": "+X right, +Y up, -Z forward",
        "ray_distance_m": depth.numpy().copy(),
        "forward_depth_m": forward_depth.numpy().copy(),
        "shape_id": ids,
        "valid_hit": ids != 0xFFFFFFFF,
        "shape_labels": {box: model.shape_label[box]},
        "no_hit_id": 0xFFFFFFFF,
    }


if __name__ == "__main__":
    main()
